#!/bin/bash
# copy.sh

#SYSTEMS=(wt n33d b3d nalld allb3d)
#SYSTEMS=(wt nalld allb3d)
#SYSTEMS=(allDb3d)
SYSTEMS=(nalld)
FF="data"
OUT_ROOT=1us
SOURCE=/home/dyang/crystallin/1hk0

for SYS in ${SYSTEMS[@]} ; do
    mkdir -p $FF/$SYS
    cd $FF/$SYS
    for VER in $(seq -f "%02g" 1 1 1) ; do
    #for VER in $(seq -f "%02g" 0 1 24) ; do
    #for VER in $(seq -f "%02g" 0 1 9) ; do
    #for VER in $(seq -f "%02g" 10 1 14) ; do
    #for VER in $(seq -f "%02g" 15 1 19) ; do
        mkdir -p v$VER/$OUT_ROOT
        #rsync -axvhP $SOURCE/$SYS/v$VER/$OUT_ROOT/*.dat v$VER/$OUT_ROOT/
        rsync -axhvP dyang@ultron.structbio.pitt.edu:$SOURCE/$SYS/v$VER/$OUT_ROOT/*.dat v$VER/$OUT_ROOT/
        #rsync -axhvP dyang@ultron.structbio.pitt.edu:$SOURCE/$SYS/v$VER/$OUT_ROOT/mmgbsa/*.dat v$VER/$OUT_ROOT/
    done
    cd ../..
done
