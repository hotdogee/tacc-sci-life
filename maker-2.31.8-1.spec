Name:       maker
Summary:    A portable and easy to configure genome annotation pipeline
Version:    2.31.8
Release:    1
License:    Perl Artistic License 2.0
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Source1:   postgresql-9.2.4.tar.gz
Patch1:    %{name}-%{version}.patch
Packager:   TACC - vaughn@tacc.utexas.edu

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}MAKER
%define PNAME       maker
# Maker is a special module. It comes bundled with a lot of
# reference data used in the annotation. That data is maintained
# on a shared directory. To ensure this policy, later on in the
# spec, an error is thrown if the data directory is not found
%define MAKER_DATADIR /scratch/projects/tacc/bio/%{name}/%{version}

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
MAKER is a portable and easily configurable genome annotation pipeline. It's purpose is to allow smaller eukaryotic and prokaryotic genome projects to independently annotate their genomes and to create genome databases. MAKER identifies repeats, aligns ESTs and proteins to a genome, produces ab-initio gene predictions and automatically synthesizes these data into gene annotations having evidence-based quality values.

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

for DIR in "" RepeatMasker RepeatMasker/rmblast blast augustus snap exonerate
do
    if [ ! -d "%{MAKER_DATADIR}/${DIR}" ]; then
        echo "%{MAKER_DATADIR}/${DIR} was not found. Aborting rpmbuild."
        exit 1
    fi
done

#chown -R root:G-800657 %{MAKER_DATADIR}/
#chmod -R 755 %{MAKER_DATADIR}

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}-%{version}
%setup -n %{name}-%{version} -T -D -a 1
%patch1 -p1

%build
%install
%include ../system-load.inc

# Load additional modules here (as needed)
module purge
module load TACC
module swap mvapich2 openmpi

CWD=`pwd`
mkdir pgsql
cd postgresql-9.2.4/
./configure --prefix=$CWD/pgsql
gmake
gmake install

cd ../src
perl Build.PL << EOF
y
/opt/apps/intel11_1/openmpi/1.4.3/bin/mpicc
/opt/apps/intel11_1/openmpi/1.4.3/include
EOF
./Build installdeps << EOF
Y
yes
yes
yes
yes
yes
yes
yes
yes
yes
y
yes
yes
yes
yes
n
a
n
yes
yes
yes
yes
yes
yes
Y
/home1/0000/build/rpms/BUILD/maker-2.28b/pgsql/bin
9
2
4
/home1/0000/build/rpms/BUILD/maker-2.28b/pgsql/bin
/home1/0000/build/rpms/BUILD/maker-2.28b/pgsql/include
/home1/0000/build/rpms/BUILD/maker-2.28b/pgsql/lib
Y
EOF

./Build install

cd $CWD
cp -R ./bin ./data ./GMOD ./lib ./LICENSE ./MWAS ./perl ./pgsql ./README $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
A portable and easy to configure genome annotation pipeline. MAKER allows smaller eukaryotic genome projects and prokaryotic genome projects to annotate their genomes and to create genome databases. MAKER identifies repeats, aligns ESTs and proteins to a genome, produces ab initio gene predictions and automatically synthesizes these data into gene annotations with evidence-based quality values. MAKER is also easily trainable: outputs of preliminary runs can be used to automatically retrain its gene prediction algorithm, producing higher quality gene-models on subsequent runs. MAKER's inputs are minimal. Its outputs are in GFF3 or FASTA format, and can be directly loaded into Chado, GBrowse, JBrowse or Apollo. Documentation can be found at http://gmod.org/wiki/MAKER.

Version %{version}
]])

whatis("Name: maker")
whatis("Version: %{version}")
whatis("Category: Biology, sequencing")
whatis("Keywords:  Genome, Sequencing, Annotation")
whatis("Description: Maker - a portable and easily configurable genome annotation pipeline.")
whatis("http://www.yandell-lab.org/software/maker.html")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
prepend_path("PATH",              "%{INSTALL_DIR}/pgsql/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
prepend_path("LD_PRELOAD",              "/opt/apps/intel11_1/openmpi/1.4.3/lib/libmpi.so")
setenv ( "OMPI_MCA_mpi_warn_on_fork",    "0")
setenv ( "TACC_MAKER_DATADIR",      "/scratch/projects/tacc/bio/%{name}/%{version}")
prepend_path("PATH",         "%{MAKER_DATADIR}/RepeatMasker")
prepend_path("PATH",         "%{MAKER_DATADIR}/RepeatMasker/rmblast/bin")
prepend_path("PATH",         "%{MAKER_DATADIR}/blast/bin")
setenv ("AUGUSTUS_CONFIG_PATH",     "%{MAKER_DATADIR}/augustus/config")
prepend_path("PATH",         "%{MAKER_DATADIR}/augustus/bin")
prepend_path("PATH",         "%{MAKER_DATADIR}/snap")
setenv ("ZOE",        "%{MAKER_DATADIR}/snap/Zoe")
prepend_path("PATH",         "%{MAKER_DATADIR}/exonerate/bin")
prereq("openmpi")

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

