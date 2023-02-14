#!/bin/bash
# multi_extend.sh
# extend prod sim for multiple (5) replicates of each system
# Takes 1 cli argument: if $1 == "run" then resubmit the failed runs

SYSTEMS=(lo_pH E175A)
PDB=2kod
PROD_NUM=07

SLURM=h2p_1gpu_prod_${PROD_NUM}.slurm

# go to target directory
for SYS in ${SYSTEMS[@]} ; do
    cd $SYS
    echo -e "\nEXTENDING SYSTEM : $SYS"

    # make the 5 replicate sub-directories
    for V in {00..04..1} ; do

        # if file is missing or file tail incorrect, run again, else skip
        if [[ -f v$V/${PROD_NUM}_prod.out && "$(tail -1 v$V/${PROD_NUM}_prod.out)" == "|  Total wall time:"* ]] ; then
            echo PROD ${PROD_NUM} FILE ALREADY FINISHED FOR ${SYS} V${V} SKIPPING
            continue

        elif [[ ! -f v$V/${PROD_NUM}_prod.out || "$(tail -1 v$V/${PROD_NUM}_prod.out)" != "|  Total wall time:"* ]] ; then
            echo PROD ${PROD_NUM} FILE ERROR FOR ${SYS} V${V}

            if [[ $1 == "run" ]] ; then
                cd v$V
                echo "GENERATING REPLICA V$V" 
        
                # set up sub-directory slurm file
                #cp -v ../../sim_template/$SLURM .
        
                # apply globally to slurm file
                #sed -i "s/PDB_TEMP/${PDB}_${SYS}/g" $SLURM
                #sed -i "s/VER/v${V}/" $SLURM
        
                # submit the extension prod run
                sbatch $SLURM
                echo -e "REPLICATE V$V FINISHED SUBMISSION\n"
                cd ..
            fi

        fi

    done

    echo "FINISHED SYSTEM : $SYS"
    cd ..
done        

