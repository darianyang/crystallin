#!/bin/bash
# multi_set_and_run.sh
# set up and run multiple (5) replicates of each system

SYSTEMS=(lo_pH E175A)
PDB=2kod

# go to target directory
for SYS in ${SYSTEMS[@]} ; do
    # make parent dir if needed
    if [ ! -d $SYS ] ; then
        mkdir $SYS
    fi
    cd $SYS
    echo "RUNNING SYSTEM : $SYS"

    # make the 5 replicate sub-directories
    for V in {01..04..1} ; do
        echo "GENERATING REPLICA V$V"
        # set up sub-directory if needed
        if [ ! -d v$V ] ; then
            mkdir v$V
        fi

        cp -v ${PDB}_${SYS}_leap.pdb v$V
        cp ../sim_template/* v$V

        cd v$V
        # formatting
        bash temp_sed.sh ${PDB}_${SYS} v$V
        # make the inital parm and crd files
        tleap -f tleap.in > tleap.out
        # submit the prep run, which submits the prod after finishing
        sbatch prep_mpi.slurm
        cd ..
    done

    echo "FINISHED SYSTEM : $SYS"
    cd ..
done        

