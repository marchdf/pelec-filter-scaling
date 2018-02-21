#!/bin/bash

run_cases () {

    # Setup
    PELECBIN=../PeleC3d.gnu.ivybridge.PROF.MPI.OMP.ex
    INAME=inputs_3d
    GPFX=grids_file_
    MGSS=(8 16 32 64)

    HYPERTHREADS=2
    TASKS_PER_NODE=2
    THREADS=$((${SLURM_CPUS_ON_NODE} / (${TASKS_PER_NODE} * ${HYPERTHREADS})))
    TASKS=$((${SLURM_JOB_NUM_NODES} * ${TASKS_PER_NODE}))
    CPUS_PER_TASKS=$((${SLURM_CPUS_ON_NODE} / ${TASKS_PER_NODE}))
    CORES=$((${TASKS} * ${THREADS}))

    # Run the scaling study
    export OMP_NUM_THREADS=${THREADS}
    export OMP_PROC_BIND=true
    export OMP_PLACES=threads
    echo "Running with ${TASKS} tasks and ${THREADS} threads on ${SLURM_JOB_NUM_NODES} nodes (${CORES} cores)"
    
    for MGS in "${MGSS[@]}"
    do
	(set -x; NCELLS=640; NLVL=0; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.max_grid_size=${MGS} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=2 > `printf "3pts_%02dmgs_%01dlvls_%08dcores.out" ${MGS} ${NLVL} ${CORES}` 2>&1 ;)
	(set -x; NCELLS=512; NLVL=1; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.max_grid_size=${MGS} amr.initial_grid_file=${GPFX}${NCELLS}_${NLVL}_${MGS} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=2 > `printf "3pts_%02dmgs_%01dlvls_%08dcores.out" ${MGS} ${NLVL} ${CORES}` 2>&1 ;)
	(set -x; NCELLS=448; NLVL=2; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.max_grid_size=${MGS} amr.initial_grid_file=${GPFX}${NCELLS}_${NLVL}_${MGS} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=2 > `printf "3pts_%02dmgs_%01dlvls_%08dcores.out" ${MGS} ${NLVL} ${CORES}` 2>&1 ;)
	(set -x; NCELLS=416; NLVL=3; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.max_grid_size=${MGS} amr.initial_grid_file=${GPFX}${NCELLS}_${NLVL}_${MGS} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=2 > `printf "3pts_%02dmgs_%01dlvls_%08dcores.out" ${MGS} ${NLVL} ${CORES}` 2>&1 ;)
    done

}
