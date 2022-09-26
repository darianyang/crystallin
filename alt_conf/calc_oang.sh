#!/bin/bash

PDBS=(1hk0_wt_leap last_frame_wt_v02 last_frame_nalld_v01)

for PDB in ${PDBS[@]} ; do

mkdir $PDB

cat << EOF > $PDB/calc_oang.cpp
parm $PDB.pdb
trajin $PDB.pdb

# single monomer vector
vector V1 :4,36@CA,C,O,N :43@CA,C,O,N
# vector with both monomers
vector V2 :4,36@CA,C,O,N :124,90@CA,C,O,N

run
writedata $PDB/oang.mol2 vectraj V1 V2 trajfmt mol2

vectormath vec1 V1 vec2 V2 out $PDB/o_angle.dat name o_angle dotangle
go
quit
EOF

cpptraj -i $PDB/calc_oang.cpp

done
