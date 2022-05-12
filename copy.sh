#!/bin/bash
# copy.sh

SYSTEMS=(wt n33d b3d nalld)
FF="data"
OUT_ROOT=1us
SOURCE=/home/dyang/crystallin/1hk0

for SYS in ${SYSTEMS[@]} ; do
    mkdir -p $FF/$SYS
    cd $FF/$SYS
    for VER in $(seq -f "%02g" 0 1 2) ; do
        mkdir v$VER
        rsync -axhvP dyang@ultron.structbio.pitt.edu:$SOURCE/$SYS/v$VER/$OUT_ROOT/*.dat v$VER/$OUT_ROOT/
        rsync -axhvP dyang@ultron.structbio.pitt.edu:$SOURCE/$SYS/v$VER/$OUT_ROOT/*.pdb v$VER/$OUT_ROOT/
        #rsync -axhvP dyang@ultron.structbio.pitt.edu:$SOURCE/$SYS/v$VER/$OUT_ROOT/mmgbsa/*.dat v$VER/$OUT_ROOT/
    done
    cd ../..
done
