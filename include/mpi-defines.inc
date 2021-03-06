# -*-rpm-spec-*-
#
# $Id$
#
#-------------------------------
# MPI Stack Family Definitions
#-------------------------------

# see rpm-dir.inc for the definition of "undefined"

%if %{undefined mpi_fam}
  %define mpi_fam error
%endif

########################################################################
##  The idea is to make all decisions in the here then mpi-load.inc 
##  is simple.
########################################################################


%if "%{is_mvapich2}" == "1" 
  %if %{undefined mpiV}
    %define mpi_label 1_9
    %define mpi_module_version 1.9a2
  %endif
  %if "%{mpiV}" == "1_9"
    %define mpi_label 1_9
    %define mpi_module_version 1.9a2
  %endif

  %define mpi_fam     mvapich2
  %define mpi_fam_ver mvapich2_%{mpi_label}
  %define mpi_module  %{mpi_fam}/%{mpi_module_version}
%endif

%if "%{is_impi}" == "1" 
  %if %{undefined mpiV}
    %define mpi_label 4_1
    %define mpi_module_version 4.1.0.024
  %endif
  %if "%{mpiV}" == "4_1"
    %define mpi_label 4_1
    %define mpi_module_version 4.1.0.024
  %endif
  %define mpi_fam     impi
  %define mpi_fam_ver impi_%{mpi_label}
  %define mpi_module  %{mpi_fam}/%{mpi_module_version}
%endif

%if "%{mpi_fam}" == "error"
  %{error: You must define which MPI you are using!}
  #exit
%endif
