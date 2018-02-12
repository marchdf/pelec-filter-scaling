#!/bin/bash

run_cases () {

    # Setup
    PELECBIN=../../PeleC3d.gnu.ivybridge.PROF.MPI.OMP.ex
    INAME=inputs_3d

    HYPERTHREADS=2
    TASKS_PER_NODE=2
    THREADS=$((${SLURM_CPUS_ON_NODE} / (${TASKS_PER_NODE} * ${HYPERTHREADS})))
    TASKS=$((${SLURM_JOB_NUM_NODES} * ${TASKS_PER_NODE}))
    CPUS_PER_TASKS=$((${SLURM_CPUS_ON_NODE} / ${TASKS_PER_NODE}))
    CORES=$((${TASKS} * ${THREADS}))

    # Cell counts
    NCELLS=320
    MINNODES=64
    NXCELLS=$((${SLURM_JOB_NUM_NODES} / ${MINNODES} * ${NCELLS}))
    XHI=$((2 * ${SLURM_JOB_NUM_NODES} / ${MINNODES} - 1))

    # Run the scaling study
    export OMP_NUM_THREADS=${THREADS}
    export OMP_PROC_BIND=true
    export OMP_PLACES=threads
    echo "Running with ${TASKS} tasks and ${THREADS} threads on ${SLURM_JOB_NUM_NODES} nodes (${CORES} cores)"
    (set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.n_cell=${NXCELLS} ${NCELLS} ${NCELLS} geometry.prob_hi=${XHI} 1.0 1.0 pelec.use_explicit_filter=0 > `printf "0pts_%08dcores.out" ${CORES}` 2>&1 ;)
    (set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.n_cell=${NXCELLS} ${NCELLS} ${NCELLS} geometry.prob_hi=${XHI} 1.0 1.0 pelec.les_filter_type=0 > `printf "1pts_%08dcores.out" ${CORES}` 2>&1 ;)
    (set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.n_cell=${NXCELLS} ${NCELLS} ${NCELLS} geometry.prob_hi=${XHI} 1.0 1.0 pelec.les_filter_fgr=2 > `printf "3pts_%08dcores.out" ${CORES}` 2>&1 ;)
    (set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.n_cell=${NXCELLS} ${NCELLS} ${NCELLS} geometry.prob_hi=${XHI} 1.0 1.0 pelec.les_filter_fgr=4 > `printf "5pts_%08dcores.out" ${CORES}` 2>&1 ;)
    (set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.n_cell=${NXCELLS} ${NCELLS} ${NCELLS} geometry.prob_hi=${XHI} 1.0 1.0 pelec.les_filter_fgr=6 > `printf "7pts_%08dcores.out" ${CORES}` 2>&1 ;)
}
