Summary:    maq - Mapping and Assembly with Quality
Name:       maq
Version:    0.7.1
Release:    1
License:    GPLv3
Vendor:     Sanger Institute
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.bz2
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot


#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
%include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME maq

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group:   Applications/Biology

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Maq is a software that builds mapping assemblies from short reads 
generated by the next-generation sequencing machines. It is particularly 
designed for Illumina-Solexa 1G Genetic Analyzer, and has preliminary 
functions to handle ABI SOLiD data.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_MAQ

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/maq-0.7.1
%setup -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Load correct compiler
%include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc
# Load additional modules here (as needed)

#-----------------------------
# Build parallel version
#-----------------------------

./configure CC=icc CXX=icpc --prefix=%{INSTALL_DIR}
make

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install
cp -rp ./scripts $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with the Intel 11.1 compiler.
This module makes available the maq executable along with the farm-run.pl, maq_eval.pl, maq.pl, and maq_plot.pl scripts.
The maq executable and scripts can be found in %{MODULE_VAR}_BIN and %{MODULE_VAR}_SCRIPTS.

Version %{version}
]])

whatis("Name: maq")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Assembly, Mapping, Genomics")
whatis("Description: maq - Mapping and Assembly with Quality")
whatis("URL: http://maq.sourceforge.net/")

setenv("%{MODULE_VAR}_DIR"    ,"%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN"    ,"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_SCRIPTS","%{INSTALL_DIR}/scripts")
prepend_path("PATH"           ,"%{INSTALL_DIR}/bin")
prepend_path("PATH"           ,"%{INSTALL_DIR}/scripts")

EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF



#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

