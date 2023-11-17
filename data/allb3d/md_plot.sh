#!/bin/bash

VER=$1

mdap -x $VER/1us/rmsd_bb.dat -y $VER/1us/o_angle.dat --xlim 0 6.5 --ylim -2 37 --xlabel "Backbone RMSD (Å)" --ylabel "Orientation Angle (°)" --style ../../gdc.mplstyle -z $VER/1us/o_angle.dat -zi 0 -pm scatter3d -sci 1 -scs 5 --cbar-label "Time (ns)"
