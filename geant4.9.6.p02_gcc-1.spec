# need --define 'is_gcc47 1' to run rpmbuild
#export RPM_BUILD_DIR=/admin/build/admin/rpms/stampede/
Summary:    geant4 -- toolkit for the simulation of the passage of particles through matter
Name:       geant4
Version:    9.6.p02
Release:    1
License:    Geant4 Software License
Group: Applications/Life Sciences
Source:     %{name}.%{version}.tar.gz

Packager:   TACC - jiao@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}.%{version}-gcc-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
%include ../system-defines.inc
%include compiler-defines.inc

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%package -n %{name}-%{comp_fam_ver}
Summary: GEANT4
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}
Geant4 is a toolkit for simulating the passage of particles through matter. It includes a complete range of functionality including tracking, geometry, physics models and hits. The physics processes offered cover a comprehensive range, including electromagnetic, hadronic and optical processes, a large set of long-lived particles, materials and elements, over a wide energy range starting, in some cases, from  and extending in others to the TeV energy range. It has been designed and constructed to expose the physics models utilised, to handle complex geometries, and to enable its easy adaptation for optimal use in different sets of applications. The toolkit is the result of a worldwide collaboration of physicists and software engineers. It has been created exploiting software engineering and object-oriented technology and implemented in the C++ programming language. It has been used in applications in particle physics, nuclear physics, accelerator design, space engineering and medical physics.
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
#%include compiler-defines.inc
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR TACC_GEANT4
%define GEANT4_DATADIR /scratch/projects/tacc/bio/%{name}/%{version}

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
if [ ! -d "%{GEANT4_DATADIR}" ]; then
    echo "The data directory %{GEANT4_DATADIR} was not found. Aborting rpmbuild."
    exit 1
fi
# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}.%{version}
# The next command unpacks Source1
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the
#        top-level build directory (i.e. as a subdirectory of the main source). 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
# setup -n %{name}.%{version} -T -D -a 8

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build   
%install

%include ../system-load.inc
%include compiler-load.inc          
module purge 
module load TACC
module swap intel gcc
module load cmake

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} ..


make -j 4 
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install

#two .sh need to be manually modified
cd $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
sed -i -e "56,65s@\$geant4_envbindir\/..\/share\/Geant4-9.6.2\/data@%{GEANT4_DATADIR}@g" geant4.sh

cd $RPM_BUILD_ROOT/%{INSTALL_DIR}/share/Geant4-9.6.2/geant4make
sed -i -e "161,170s@\$geant4make_root\/..\/data@%{GEANT4_DATADIR}@g" geant4make.sh
# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with cmake.
This module makes available the geant4 executable. Documentation for %{name} is available online at the publisher\'s website: http://geant4.cern.ch//
To run geant4, two bash scripts have to be sourced first. 
   cd $TACC_GEANT4_DIR/bin
   source ./geant4.sh
   cd $TACC_Geant4_DIR/share/Geant4-9.6.2/geant4make/
   source geant4make.sh

When compile code, do "cmake -DGeant4_DIR=$TACC_GEANT4_DIR/lib64/Geant4-9.6.2 ../"


Version %{version}
]])

whatis("Name: geant4")
whatis("Version: %{version}")
whatis("Category: computational biology, simulation")
whatis("Keywords:  Biology, Detector simulation, High energy, Nuclear Physics")
whatis("Description: geant4 - Toolkit for the simulation of the passage of particles through matter. ")
whatis("URL: http://geant4.cern.ch")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv (     "TACC_GEANT4_DATADIR",  "/scratch/projects/tacc/bio/%{name}/%{version}")
setenv ( "G4LEVELGAMMADATA",    "%{TACC_GEANT4_DATADIR}/PhotonEvaporation2.3")
setenv ( "G4RADIOACTIVEDATA",    "%{TACC_GEANT4_DATADIR}/RadioactiveDecay3.6")
setenv ( "G4LEDATA",    "%{TACC_GEANT4_DATADIR}/G4EMLOW6.32")
setenv ( "G4NEUTRONHPDATA",    "%{TACC_GEANT4_DATADIR}/G4NDL4.2")
setenv ( "G4ABLADATA",    "%{TACC_GEANT4_DATADIR}/G4ABLA3.0")
setenv ( "G4REALSURFACEDATA",    "%{TACC_GEANT4_DATADIR}/RealSurface1.0")
setenv ( "G4NEUTRONXSDATA",    "%{TACC_GEANT4_DATADIR}/G4NEUTRONXS1.2")
setenv ( "G4PIIDATA",    "%{TACC_GEANT4_DATADIR}/G4PII1.3")
setenv ( "G4SAIDXSDATA",    "%{TACC_GEANT4_DATADIR}/G4SAIDDATA1.1")
prereq ("cmake")

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
%files -n %{name}-%{comp_fam_ver}

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

