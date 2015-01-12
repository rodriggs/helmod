%define __os_install_post %{nil}



#------------------- package info ----------------------------------------------

#
# FIXME
#
# enter the simple app name, e.g. myapp
#
Name: %{getenv:NAME}

#
# FIXME
#
# enter the app version, e.g. 0.0.1
#
Version: %{getenv:VERSION}

# FIXME
#
# enter the base release; start with fasrc01 and increment in subsequent 
# releases; the actual "Release" is constructed dynamically and set below
#
%define release_short %{getenv:RELEASE}

#
# FIXME
#
# enter your FIRST LAST <EMAIL>
#
Packager: %{getenv:FASRCSW_AUTHOR}

#
# FIXME
#
# enter a succinct one-line summary (%%{summary} gets changed when the debuginfo 
# rpm gets created, so this stores it separately for later re-use)
#
%define summary_static Intel Cluster Studio XE 2015 High Performance MPI Hybrid Cluster Development Suite
Summary: %{summary_static}

#
# FIXME
#
# enter the url from where you got the source, as a comment; change the archive 
# suffix if applicable
#
#(not applicable)
Source: %{name}-%{version}.tar.bz2

#
# there should be no need to change the following
#

#these fields are required by RPM
Group: fasrcsw
License: see COPYING file or upstream packaging

#this comes here since it uses Name and Version but dynamically computes Release, Prefix, etc.
%include fasrcsw_defines.rpmmacros

Release: %{release_full}
Prefix: %{_prefix}


#
# FIXME
#
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
High Performance Comprehensive Cluster Development Tools for HPC.
Scale Development Efforts with Standards Driven Compilers, Programming Models and Tools.
Supports the Latest Multicore and Manycore Based Systems.
To use vtune, inspector or advisor, source the appropriate *vars.sh file:
vtune      source amplxe-vars.sh
inspector  source inspxe-vars.sh
advisor    source advixe-vars.sh



#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep

#
# FIXME
#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things
#

#%%setup




#------------------- %%build (~ configure && make) ----------------------------

%build

#
# FIXME
#
# configure and make the software here; the default below is for standard 
# GNU-toolchain style things
# 

#(leave this here)
%include fasrcsw_module_loads.rpmmacros

##prerequisite apps (uncomment and tweak if necessary)
#module load NAME/VERSION-RELEASE

#%%configure
#make



#------------------- %%install (~ make install + create modulefile) -----------

%install

#
# FIXME
#
# make install here; the default below is for standard GNU-toolchain style 
# things; plus we add some handy files (if applicable) and build a modulefile
#

#(leave this here)
%include fasrcsw_module_loads.rpmmacros

#%%makeinstall
#echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
#rsync -av %{_topdir}/BUILD/%{name}-%{version}/ %{buildroot}/%{_prefix}/

#these files are nice to have; %%doc is not as prefix-friendly as I would like
#if there are other files not installed by make install, add them here
for f in COPYING AUTHORS README INSTALL ChangeLog NEWS THANKS TODO BUGS; do
	test -e "$f" && ! test -e '%{buildroot}/%{_prefix}/'"$f" && cp -a "$f" '%{buildroot}/%{_prefix}/'
done

#this is the part that allows for inspecting the build output without fully creating the rpm
#there should be no need to change this
%if %{defined trial}
	set +x
	
	echo
	echo
	echo "*************** fasrcsw -- STOPPING due to %%define trial yes ******************"
	echo 
	echo "Look at the tree output below to decide how to finish off the spec file.  (\`Bad"
	echo "exit status' is expected in this case, it's just a way to stop NOW.)"
	echo
	echo
	
	tree '%{buildroot}/%{_prefix}'

	echo
	echo
	echo "******************************************************************************"
	echo
	echo
	
	#make the build stop
	false

	set -x
%endif

# 
# FIXME (but the above is enough for a "trial" build)
#
# - uncomment any applicable prepend_path things
#
# - do any other customizing of the module, e.g. load dependencies
#
# - in the help message, link to website docs rather than write anything 
#   lengthy here
#
# references on writing modules:
#   http://www.tacc.utexas.edu/tacc-projects/lmod/advanced-user-guide/writing-module-files
#   http://www.tacc.utexas.edu/tacc-projects/lmod/system-administrator-guide/initial-setup-of-modules
#   http://www.tacc.utexas.edu/tacc-projects/lmod/system-administrator-guide/module-commands-tutorial
#
cat > %{buildroot}/%{_prefix}/modulefile.lua <<EOF
local helpstr = [[
%{name}-%{version}-%{release_short}
%{summary_static}
]]
help(helpstr,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}-%{release_short}")
whatis("Description: %{summary_static}")

---- prerequisite apps (uncomment and tweak if necessary)
--if mode()=="load" then
--	if not isloaded("NAME") then
--		load("NAME/VERSION-RELEASE")
--	end
--end

---- environment changes (uncomment what is relevant)


setenv("CC" , "icc")
setenv("CXX", "icpc")
setenv("FC" , "ifort")
setenv("F77", "ifort")

setenv("INTEL_HOME",                "/n/sw/intel-cluster-studio-2015")
setenv("INTEL_LIB",                 "/n/sw/intel-cluster-studio-2015/lib/intel64")
setenv("INTEL_LICENSE_FILE",        "/n/sw/intel-cluster-studio-2015/license")
setenv("INTEL_COMPOSER_INCLUDE",    "/n/sw/intel-cluster-studio-2015/composerxe/include")
setenv("MKL_HOME",                  "/n/sw/intel-cluster-studio-2015/mkl")
setenv("TBB_HOME",                  "/n/sw/intel-cluster-studio-2015/tbb")
prepend_path("PATH",                "/n/sw/intel-cluster-studio-2015/bin")
prepend_path("LD_LIBRARY_PATH",     "/n/sw/intel-cluster-studio-2015/lib/intel64")
prepend_path("LD_LIBRARY_PATH",     "/n/sw/intel-cluster-studio-2015/mkl/lib/intel64")
prepend_path("LD_LIBRARY_PATH",     "/n/sw/intel-cluster-studio-2015/tbb/lib/intel64")
prepend_path("LIBRARY_PATH",        "/n/sw/intel-cluster-studio-2015/lib/intel64")
prepend_path("LIBRARY_PATH",        "/n/sw/intel-cluster-studio-2015/mkl/lib/intel64")
prepend_path("LIBRARY_PATH",        "/n/sw/intel-cluster-studio-2015/tbb/lib/intel64")
prepend_path("MANPATH",             "/n/sw/intel-cluster-studio-2015/man/en_US")

---- Support for starting vtune, etc.  Just source the appropriate vars.sh
prepend_path("PATH",                "/n/sw/intel-cluster-studio-2015/vtune_amplifier_xe")
prepend_path("PATH",                "/n/sw/intel-cluster-studio-2015/inspector_xe")
prepend_path("PATH",                "/n/sw/intel-cluster-studio-2015/advisor_xe")

local mroot = os.getenv("MODULEPATH_ROOT")
local mdir = pathJoin(mroot, "Comp/%{name}/%{version}-%{release_short}")
prepend_path("MODULEPATH", mdir)
setenv("FASRCSW_COMP_NAME"   , "%{name}")
setenv("FASRCSW_COMP_VERSION", "%{version}")
setenv("FASRCSW_COMP_RELEASE", "%{release_short}")
family("Comp")
EOF



#------------------- %%files (there should be no need to change this ) --------

%files

%defattr(-,root,root,-)

%{_prefix}/*



#------------------- scripts (there should be no need to change these) --------


%pre
#
# everything in fasrcsw is installed in an app hierarchy in which some 
# components may need creating, but no single rpm should own them, since parts 
# are shared; only do this if it looks like an app-specific prefix is indeed 
# being used (that's the fasrcsw default)
#
echo '%{_prefix}' | grep -q '%{name}.%{version}' && mkdir -p '%{_prefix}'
#

%post
#
# symlink to the modulefile installed along with the app; we want all rpms to 
# be relocatable, hence why this is not a proper %%file; as with the app itself, 
# modulefiles are in an app hierarchy in which some components may need 
# creating
#
mkdir -p %{modulefile_dir}
ln -s %{_prefix}/modulefile.lua %{modulefile}
#


%preun
#
# undo the module file symlink done in the %%post; do not rmdir 
# %%{modulefile_dir}, though, since that is shared by multiple apps (yes, 
# orphans will be left over after the last package in the app family 
# is removed)
#
test -L '%{modulefile}' && rm '%{modulefile}'
#

%postun
#
# undo the last component of the mkdir done in the %%pre (yes, orphans will be 
# left over after the last package in the app family is removed); also put a 
# little protection so this does not cause problems if a non-default prefix 
# (e.g. one shared with other packages) is used
#
test -d '%{_prefix}' && echo '%{_prefix}' | grep -q '%{name}.%{version}' && rmdir '%{_prefix}'
#


%clean
#
# wipe out the buildroot, but put some protection to make sure it isn't 
# accidentally / or something -- we always have "rpmbuild" in the name
#
echo '%{buildroot}' | grep -q 'rpmbuild' && rm -rf '%{buildroot}'
#
