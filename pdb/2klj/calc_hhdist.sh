#!/bin/bash
# make a chimeraX command script (.cxc)
# for calculating the H-H distances
# of all 10 solution state models

script_name="calc_hhdist.cxc"

for i in {1..10} ; do
    echo -e "distance #1.${i}/A:84@CB #1.${i}/A:88@CB \n" >> $script_name
done
