Summary:    SMRT Analysis Suite
Name:       smrt
Version:    2.3.0.140936.p0
Release:    1
License:    GPL
Vendor:     PacBio
Group: Applications/Life Sciences
Source:     smrtanalysis_%{version}.tar.gz
Packager:   TACC - gzynda@tacc.utexas.edu
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%include ../rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define APPS    /opt/apps
%define MODULES modulefiles
%define INSTALL_DIR /share1/apps/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define PNAME %{name}
%define MODULE_VAR TACC_SMRT

%define __os_install_post    \
    /usr/lib/rpm/redhat/brp-compress \
    %{!?__debug_package:/usr/lib/rpm/redhat/brp-strip %{__strip}} \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
%{nil}


%description
The SMRT Analysis software suite performs assembly and variant detection analysis of sequencing data generated by the Pacific Biosciences instrument.

## PREP
%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}
%setup -n %{PNAME}-%{version}

%build
%include ../system-load.inc

%install
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r smrtanalysis $RPM_BUILD_ROOT/%{INSTALL_DIR}/

##################################################
#	Module Section
##################################################
# ADD ALL MODULE STUFF HERE
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
Documentation for %{PNAME} is available online at the publisher website: https://github.com/PacificBiosciences/SMRT-Analysis

To use interactively, run:
	smrtshell

To run though a job script, run:
	smrtpipe

Automatic job submission is not currently supported, but more information about running analyses can be found at: https://github.com/PacificBiosciences/SMRT-Analysis/wiki/SMRT-Pipe-Reference-Guide-v2.3.0

For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PATH has been updated to include smrtcmds.

Version %{version}
]])
whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics, qc, assembly")
whatis("Keywords: pacbio, smrt")
whatis("Description: SMRT Analysis Suite - Suite for processing PacBio data")
whatis("URL: https://github.com/PacificBiosciences/SMRT-Analysis")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
setenv("SMRT_ROOT","%{INSTALL_DIR}/smrtanalysis")
prepend_path("PATH","%{INSTALL_DIR}/smrtanalysis/smrtcmds/bin")
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
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}