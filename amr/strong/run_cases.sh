#!/bin/bash

run_cases () {
    (set -x; ls -alh ${SLURM_CPUS_ON_NODE})
    (set -x; ls -alh ${SLURM_JOB_NUM_NODES})

    # Setup
    PELECBIN=../../PeleC3d.gnu.ivybridge.PROF.MPI.OMP.ex
    INAME=inputs_3d
    GPFX=grids_file_640_
    NLVLS=(1 2 3)

    HYPERTHREADS=2
    TASKS_PER_NODE=2
    THREADS=${SLURM_CPUS_ON_NODE} / ${TASKS_PER_NODE}
    TASKS=$((${SLURM_JOB_NUM_NODES} * ${TASKS_PER_NODE}))
    CPUS_PER_TASKS=$((${HYPERTHREADS} * ${THREADS}))
    NPROCS=$((${TASKS} * ${THREADS}))

    # Cell counts
    NCELLS=640



    # Run the scaling study
    export OMP_NUM_THREADS=${THREADS}
    export OMP_PROC_BIND=true
    export OMP_PLACES=threads
    echo "Running with ${TASKS} tasks and ${THREADS} threads on ${SLURM_JOB_NUM_NODES} nodes (${NPROCS} procs)"
    for NLVL in "${NLVLS[@]}"
    do
        echo "Running with ${NRANK} ranks and ${THREADS} threads (${NPROC} procs) and ${NLVL} levels"
        
        srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.initial_grid_file=${GPFX}${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.use_explicit_filter=0 > `printf "0pts_%01dlvls_%08dprocs.out" ${NLVL} ${NPROC}` 2>&1 ;
        srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.initial_grid_file=${GPFX}${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_type=0 > `printf "1pts_%01dlvls_%08dprocs.out" ${NLVL} ${NPROCS}` 2>&1 ;
        srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.initial_grid_file=${GPFX}${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=2 > `printf "3pts_%01dlvls_%08dprocs.out" ${NLVL} ${NPROCS}` 2>&1 ;
        srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.initial_grid_file=${GPFX}${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=4 > `printf "5pts_%01dlvls_%08dprocs.out" ${NLVL} ${NPROCS}` 2>&1 ;
        srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.initial_grid_file=${GPFX}${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=6 > `printf "7pts_%01dlvls_%08dprocs.out" ${NLVL} ${NPROCS}` 2>&1 ;
    done



}
