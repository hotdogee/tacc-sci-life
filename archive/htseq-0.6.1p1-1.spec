Summary:    HTSeq
Name:       htseq
Version:    0.6.1p1
Release:    1
License:    GPL
Vendor:     EMBL
Group: Applications/Life Sciences
Source:     HTSeq-%{version}.tar.gz
Packager:   TACC - jawon@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%include ../rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME htseq
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_HTSEQ

%description
HTSeq is a Python package that provides infrastructure to process data from high-throughput sequencing assays

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -n HTSeq-%{version}
%build
%install
%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

module load python
which python
python setup.py build
mkdir -p $PWD/lib/python2.7/site-packages/
python setup.py install --user
cp -r /home1/02114/wonaya/.local/lib/python2.7/site-packages/HTSeq-%{version}-py2.7-linux-x86_64.egg $PWD/lib/python2.7/site-packages/.
chmod a+rx $PWD/scripts/*
cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'


help (
[[
This module loads %{PNAME}, which depends on python and numpy.
To call this function, use htseq-count
Documentation for %{PNAME} is available online at the publisher website: http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PYTHONPATH has been prepended to include the HTSeq library.
Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, High-throughput Sequencing")
whatis("Description: HTSeq - Analysing high-throughput sequencing data with Python")
whatis("URL: https://pypi.python.org/pypi/HTSeq")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PYTHONPATH","%{INSTALL_DIR}/lib/python2.7/site-packages/HTSeq-%{version}-py2.7-linux-x86_64.egg/")
prepend_path("PATH","%{INSTALL_DIR}/scripts")
prereq("python")

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


module unload python

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

