#!/bin/bash

run_cases () {

    # Setup
    PELECBIN=../../PeleC3d.gnu.ivybridge.PROF.MPI.OMP.ex
    INAME=inputs_3d
    NLVLS=(1)

    HYPERTHREADS=2
    TASKS_PER_NODE=2
    THREADS=$((${SLURM_CPUS_ON_NODE} / (${TASKS_PER_NODE} * ${HYPERTHREADS})))
    TASKS=$((${SLURM_JOB_NUM_NODES} * ${TASKS_PER_NODE}))
    CPUS_PER_TASKS=$((${SLURM_CPUS_ON_NODE} / ${TASKS_PER_NODE}))
    CORES=$((${TASKS} * ${THREADS}))

    # Cell counts
    NCELLS=64



    # Run the scaling study
    export OMP_NUM_THREADS=${THREADS}
    export OMP_PROC_BIND=true
    export OMP_PLACES=threads
    for NLVL in "${NLVLS[@]}"
    do
	echo "Running ${NLVL} levels with ${TASKS} tasks and ${THREADS} threads on ${SLURM_JOB_NUM_NODES} nodes (${CORES} cores)"

        #(set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.max_level=${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.use_explicit_filter=0 > `printf "0pts_%01dlvls_%08dcores.out" ${NLVL} ${CORES}` 2>&1 ;)
        #(set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.max_level=${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_type=0 amr.restart=./restart/chk01000 max_step=1010 > `printf "1pts_%01dlvls_%08dcores.out" ${NLVL} ${CORES}` 2>&1 ;)
        (set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.max_level=${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=2 amr.restart=./restart/chk01000 max_step=1010 > `printf "3pts_%01dlvls_%08dcores.out" ${NLVL} ${CORES}` 2>&1 ;)
        #(set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.max_level=${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=4 > `printf "5pts_%01dlvls_%08dcores.out" ${NLVL} ${CORES}` 2>&1 ;)
        #(set -x; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets ${PELECBIN} ${INAME} amr.max_level=${NLVL} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=6 > `printf "7pts_%01dlvls_%08dcores.out" ${NLVL} ${CORES}` 2>&1 ;)
    done
}
