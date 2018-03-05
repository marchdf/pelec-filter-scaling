#!/bin/bash

run_cases () {

    # Setup
    PELECBIN=../PeleC3d.intel.ivybridge.PROF.MPI.OMP.ex
    INAME=inputs_3d
    NID=`hostname`

    HYPERTHREADS=2
    TASKS_PER_NODE=2
    THREADS=$((${SLURM_CPUS_ON_NODE} / (${TASKS_PER_NODE} * ${HYPERTHREADS})))
    TASKS=$((${SLURM_JOB_NUM_NODES} * ${TASKS_PER_NODE}))
    CPUS_PER_TASKS=$((${SLURM_CPUS_ON_NODE} / ${TASKS_PER_NODE}))
    CORES=$((${TASKS} * ${THREADS}))

    # Cell counts
    NCELLS=120



    # Run the scaling study
    export OMP_NUM_THREADS=${THREADS}
    export OMP_PROC_BIND=true
    export OMP_PLACES=threads
    echo "Running with ${TASKS} tasks and ${THREADS} threads on ${SLURM_JOB_NUM_NODES} nodes (${CORES} cores)"
    
    (set -x; RDIR="0pts"; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets amplxe-cl -collect memory-access -knob analyze-mem-objects=true -r ${RDIR} -trace-mpi -- ${PELECBIN} ${INAME} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.use_explicit_filter=0 > `printf "0pts_%08dcores.out" ${CORES}` 2>&1 ; amplxe-cl -R hotspots -result-dir ${RDIR}.${NID} -format=csv &> 0pts_profile_memory.txt; )
    (set -x; RDIR="1pts"; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets amplxe-cl -collect memory-access -knob analyze-mem-objects=true -r ${RDIR} -trace-mpi -- ${PELECBIN} ${INAME} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_type=0 > `printf "1pts_%08dcores.out" ${CORES}` 2>&1 ; amplxe-cl -R hotspots -result-dir ${RDIR}.${NID} -format=csv &> 1pts_profile_memory.txt; )
    (set -x; RDIR="3pts"; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets amplxe-cl -collect memory-access -knob analyze-mem-objects=true -r ${RDIR} -trace-mpi -- ${PELECBIN} ${INAME} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=2 > `printf "3pts_%08dcores.out" ${CORES}` 2>&1 ; amplxe-cl -R hotspots -result-dir ${RDIR}.${NID} -format=csv &> 3pts_profile_memory.txt; )
    (set -x; RDIR="5pts"; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets amplxe-cl -collect memory-access -knob analyze-mem-objects=true -r ${RDIR} -trace-mpi -- ${PELECBIN} ${INAME} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=4 > `printf "5pts_%08dcores.out" ${CORES}` 2>&1 ; amplxe-cl -R hotspots -result-dir ${RDIR}.${NID} -format=csv &> 5pts_profile_memory.txt; )
    (set -x; RDIR="7pts"; srun -n ${TASKS} -c ${CPUS_PER_TASKS} --cpu_bind=sockets amplxe-cl -collect memory-access -knob analyze-mem-objects=true -r ${RDIR} -trace-mpi -- ${PELECBIN} ${INAME} amr.n_cell=${NCELLS} ${NCELLS} ${NCELLS} pelec.les_filter_fgr=6 > `printf "7pts_%08dcores.out" ${CORES}` 2>&1 ; amplxe-cl -R hotspots -result-dir ${RDIR}.${NID} -format=csv &> 7pts_profile_memory.txt; )
}
