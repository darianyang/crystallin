parm last_frame_nalld_v01.pdb
trajin last_frame_nalld_v01.pdb

# single monomer vector
vector V1 :4,36@CA,C,O,N :43@CA,C,O,N
# vector with both monomers
vector V2 :4,36@CA,C,O,N :124,90@CA,C,O,N

run
writedata last_frame_nalld_v01/oang.mol2 vectraj V1 V2 trajfmt mol2

vectormath vec1 V1 vec2 V2 out last_frame_nalld_v01/o_angle.dat name o_angle dotangle
go
quit
