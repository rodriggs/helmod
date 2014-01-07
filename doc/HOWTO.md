# How to build and install an app


## Overview

The basic workflow of fasrcsw is:

* get the source
* create and partially complete a spec file, using the template as a starting point
* do a preliminary build of the software to see what it creates, in order to know what to put in the module file
* complete the spec file and build the final rpm(s)
* install the rpm(s)
* commit changes and move the build outputs to production locations

The default behavior and templates are designed to work with GNU-toolchain-style software packages, i.e. things that use `configure`/`make`/`make install` with standard options, with as little modification as possible.
As an example, this document uses the automake hello-world example, `amhello-1.0.tar.gz`, distributed with automake.


## Prep

Get ready to build software:

* make sure you've cloned and configured fasrcsw according to [this](INSTALL.md#have-each-contributor-setup-a-development-repo-clone)
* make sure you're logged into the build host
* make sure you're logged into your normal user account, *not* root

`cd` to your personal fasrcsw clone.
Make sure your clone is up-to-date and your environment is pristine, and setup the environment:

``` bash
git pull
module purge
source ./setup.sh
```

There will now be two environment variables defined that are used in the instructions below --
`$FASRCSW_DEV` is the location of your personal clone, and
`$FASRCSW_PROD` is the one, central location for your organizations's software.

In order to be able to copy-n-paste commands below, set these variables particular to the app you're installing:

``` bash
NAME=...
VERSION=...
RELEASE=...
TYPE=...
```

These variables are only used by this doc, not fasrcsw.
`NAME` and `VERSION` are whatever the app claims, though some adjustements may be required -- see [this FAQ item](FAQ.md#what-are-the-naming-conventions-and-restrictions-for-an-apps-name-version-and-release).
`RELEASE` is used to track the build under the fasrcsw system and should be of the form `fasrc##` where `##` is a two-digit number.
If this is the first fasrcsw-style build, use `fasrc01`; otherwise increment the fasrc number used in the previous spec file for the app.

Regarding `TYPE`, a major purpose of fasrcsw is to manage entire software environments for multiple compiler and MPI implementations.
Apps are therefore categorized by their *dependencies* (see [this FAQ item](FAQ.md#why-is-a-compiler-a-core-app-and-not-a-comp-app-why-is-an-mpi-implementation-a-comp-app-and-not-an-mpi-app) more about this initially non-intuitive convention, adopted from TACC):

* A *Core* app is one that does not depend on a compiler or MPI implementation.  The compilers themselves, and their dependencies, are core apps, but that's about it.
* A *Comp* app is one that depends upon compiler but not MPI implementation.  The MPI apps themselves are *Comp* apps, as are almost all general, non-mpi-enabled apps.
* A *MPI* app is one that depends upon MPI implementation, and therefore upon compiler, too.

Thefore, set `TYPE` to the string `Core`, `Comp`, or `MPI`.

E.g. to test the simple *Core* case with `amhello`: `NAME=amhello ; VERSION=1.0 ; RELEASE=fasrc01 ; TYPE=Core`.
However, if multiple admins are trying this taste case at the same time, you should make an exception and set RELEASE to $USER so people are not clobbering each other.
The `amhello` example can be used to test all app types, even though the dependencies are not real.



## Get the source code

By whatever means necessary, get a copy of the app source archive into the location for the sources.
E.g.:

``` bash
cd "$FASRCSW_DEV"/rpmbuild/SOURCES
wget --no-clobber http://...
```

For `amhello`, which is a bit complicated because it's a tarball within another tarball: curl http://ftp.gnu.org/gnu/automake/automake-1.14.tar.xz | tar --strip-components=2 -xvJf - automake-1.14/doc/amhello-1.0.tar.gz


## Create a preliminary spec file

Change to the directory of spec files:

``` bash
cd "$FASRCSW_DEV"/rpmbuild/SPECS
```

Create a spec file for the app based upon the template:

``` bash
cp -ai template.spec "$NAME-$VERSION-$RELEASE".spec
```

Now edit the spec file:

``` bash
$EDITOR "$NAME-$VERSION-$RELEASE".spec
```

and address things with the word `FIXME` in them.
For some things, the default will be fine.
Eventually all need to be addressed, but for now, just complete everything up to where `modulefile.lua` is created.
The next step will provide the necessary guidance on what to put in the module file.

If the app you're building requires other apps, follow the templates for loading the appropriate modules during the `%build` step and having the module file require them, too.
See [this FAQ item](FAQ.md#how-are-simple-app-dependencies-handled) for more details.

If you need to add options to the `./configure` command, you can append them to the `%configure` macro.
If the build procedure is very different from a standard `configure`/`make`/`make install`, you'll have to manually code the corresponding steps -- see [this FAQ item](FAQ.md#how-do-i-compile-manually-instead-of-using-the-rpmbuild-macros) for details.
If it's different for different compilers and/or MPI implementations, see [this FAQ item](FAQ.md#how-do-i-use-one-spec-file-to-handle-all-compiler-and-MPI-implementations).



## Do a trial build and inspect its output

The result of the above will be enough of a spec file to basically build the software.
However, you have to build it and examine its output in order to know what to put in the module file that the rpm is also responsible for constructing.
The template spec has a section that, if the macro `inspect` is defined, will quit the rpmbuild during the `%install` step and use the `tree` command to dump out what was built and will be installed.

There are also three different scripts depending on the type of app being built -- `fasrcsw-rpmbuild-Core`, `fasrcsw-rpmbuild-Comp`, and `fasrcsw-rpmbuild-MPI`.
Putting all this together, to try building the rpm, run the following:

``` bash
fasrcsw-rpmbuild-$TYPE --define 'inspect yes' -ba "$NAME-$VERSION-$RELEASE".spec
```

Eventually, after a few iterations of running the above and tweaking the spec file in order to get the software to build properly and even get to the *inspect* step, the output will show something like this near the end:

```
*************** fasrcsw -- STOPPING due to %define inspect yes ****************


Look at the tree output below to decide how to finish off the spec file.  (`Bad
exit status' is expected in this case, it's just a way to stop NOW.)


/home/me/rpmbuild/BUILDROOT/amhello-1.0-fasrc01.x86_64//n/sw/fasrcsw/apps/Core/amhello/1.0-fasrc01
|-- README
|-- bin
|   `-- hello
`-- share
	`-- doc
		`-- amhello
			`-- README

4 directories, 3 files


******************************************************************************


error: Bad exit status from /var/tmp/rpm-tmp.B5l2ZA (%install)


RPM build errors:
	Bad exit status from /var/tmp/rpm-tmp.B5l2ZA (%install)
```

The `Bad exit status` is expected in this case.
The `README` and other docs in the root of the installation is something manually done by fasrcsw just out of personal preference.

The `fasrcsw-rpmbuild-Comp` and `fasrcsw-rpmbuild-MPI` scripts loop over the corresponding modules to be built against.
To debug just one combination, see [this FAQ item](FAQ.md#how-do-i-build-against-just-one-compiler-or-MPI-implementation-instead-of-all).


## Finish the spec file

Re-open the spec file for editing:

``` bash
$EDITOR "$NAME-$VERSION-$RELEASE".spec
```

and, based upon the output in the previous step, write what goes in `modulefile.lua`.
Some common things are already there as comments (`--` delimits a comment in lua).


## Build the rpm(s)

Now the rpm (or set of rpms) can be fully built:

``` bash
fasrcsw-rpmbuild-$TYPE -ba "$NAME-$VERSION-$RELEASE".spec
```

Once that works, double check that all worked as expected.
For a Core app, only one rpm is built, but for Comp and MPI apps, multiple rpms are built.
There are three helpers that print the names of the rpms that should've been built -- `fasrcsw-list-Core-rpms`, `fasrcsw-list-Comp-rpms`, and `fasrcsw-list-MPI-rpms`.

``` bash
fasrcsw-rpm -qilp --scripts $(fasrcsw-list-$TYPE-rpms "$NAME-$VERSION-$RELEASE") | less
```


For each package make sure:

* all the metadata looks good
* all files are under an app-specific prefix under `$FASRCSW_PROD`. 
* the module file symlink (second ln arg in postinstall scriptlet) is good

Test if the rpm(s) will install okay:

``` bash
sudo -E fasrcsw-rpm -ivh --nodeps --test $(fasrcsw-list-$TYPE-rpms "$NAME-$VERSION-$RELEASE")
```


## Install the rpm(s)

Finally, install the rpm(s):

``` bash
sudo -E fasrcsw-rpm -ivh --nodeps $(fasrcsw-list-$TYPE-rpms "$NAME-$VERSION-$RELEASE")
```

Check that it installed and the module is there.
For a *Core* app:

``` bash
fasrcsw-rpm -q "$NAME-$VERSION-$RELEASE"
ls "$FASRCSW_PROD/apps/Core/$NAME/$VERSION-$RELEASE/"
module avail
module load $NAME/$VERSION-$RELEASE
#...test the app itself...
module unload $NAME/$VERSION-$RELEASE
```

If you want to erase and retry a *Core* app: sudo -E fasrcsw-rpm -ev --nodeps "$NAME-$VERSION-$RELEASE".x86\_64


## Save your work

Copy the rpms to the production location:

``` bash
rsync -avu {"$FASRCSW_DEV","$FASRCSW_PROD"}/rpmbuild/SOURCES/
rsync -avu {"$FASRCSW_DEV","$FASRCSW_PROD"}/rpmbuild/RPMS/
rsync -avu {"$FASRCSW_DEV","$FASRCSW_PROD"}/rpmbuild/SRPMS/
```

Add, commit, and push all your modifications to the fasrcsw git remote repo with something like the following:

``` bash
cd "$FASRCSW_DEV"
git add .
git commit -v .
git pull
git push
```

And, as root, pull them to the production clone:

``` bash
cd "$FASRCSW_PROD"
sudo git pull
```