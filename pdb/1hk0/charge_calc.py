"""
Take FASTA (later also PDB) file and calculate net charge based off of pH and res identity.
"""

# 1hk0 sequence
seq = "GKITLYEDRGFQGRHYECSSDHPNLQPYLSRCNSARVDSGCWMLYEQPNYSGLQYFLRRGDYADHQQWMGLSDSVRSCRLIPHSGSHRIRLYEREDYRGQMIEFTEDCSCLQDRFRFNEIHSLNVLEGSWVLYELSNYRGRQYLLMPGDYRRYQDWGATNARVGSLRRVIDFS"
seq_list = [char for char in seq]

def fasta_charge_calc(seq_list, pH):
    """
    Input a list of 1 letter code residues for a protein and a pH float.
    Outputs the net charge (int). 
    Only will work within pH 2 - 10 (COOH - NH3).
    """
    charge = 0

    for i in seq_list:
        # handle basic residues - include histidine if pH <= 6.0 (HIS pKa = 6.04)
        if float(pH) <= 6.0 and i == "R" or i == "H" or i == "K":
            charge += 1
        # at pH > 6.0, HIS is deprotonated and neutral
        elif float(pH) > 6.0 and i == "R" or i == "H" or i == "K":
            charge += 1
        # acidic residues
        elif i == "D" or i == "E":
            charge -= 1
    
    return charge

print(fasta_charge_calc(seq_list, 6.0))