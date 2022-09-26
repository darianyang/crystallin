parm 1hk0_wt_leap.pdb
trajin 1hk0_wt_leap.pdb

# single monomer vector
vector V1 :4,36@CA,C,O,N :43@CA,C,O,N
# vector with both monomers
vector V2 :4,36@CA,C,O,N :124,90@CA,C,O,N

run
writedata 1hk0_wt_leap/oang.mol2 vectraj V1 V2 trajfmt mol2

vectormath vec1 V1 vec2 V2 out 1hk0_wt_leap/o_angle.dat name o_angle dotangle
go
quit
