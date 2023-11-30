
import numpy as np
import matplotlib.pyplot as plt

dmat_path = "data/nalld/v01/1us"

dmat1 = np.loadtxt(f"{dmat_path}/neg_dmat100.dat")
dmat1000 = np.loadtxt(f"{dmat_path}/neg_dmat1000.dat")

# columns are CTD and rows are NTD
ntd_negs = [7, 8, 17, 21, 24, 33, 38, 46, 49, 61, 64, 73]
ctd_negs = [93, 95, 96, 103, 106, 107, 113, 118, 119, 124, 127, 134, 137, 149, 155, 160, 171]

def plot_1_v_1000(): 
    gs_kw = dict(width_ratios=[1, 1, 0.06])
    fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(8,4), gridspec_kw=gs_kw)
    fig.subplots_adjust(wspace=0.3)
    p1 = ax[0].pcolormesh(dmat1, vmin=0, vmax=20)
    p1000 = ax[1].pcolormesh(dmat1000, vmin=0, vmax=20)
    cbar = fig.colorbar(p1, cax=ax[2])
    cbar.set_label("Distance ($\AA$)", labelpad=15)
    fig.supxlabel("Residue Number", x=0.48, y=0.04)
    fig.supylabel("Residue Number", x=0.01, y=0.55)
    
    # xtick formatting
    ax[0].set_xticklabels(ctd_negs, rotation=45)
    ax[0].set_xticks([i + 0.5 for i in range(0, len(ctd_negs))])
    ax[1].set_xticklabels(ctd_negs, rotation=45)
    ax[1].set_xticks([i + 0.5 for i in range(0, len(ctd_negs))])

    # ytick formattting
    ax[0].set_yticklabels(ntd_negs)
    ax[0].set_yticks([i + 0.5 for i in range(0, len(ntd_negs))])
    ax[1].set_yticklabels([])
    ax[1].set_yticks([])

    # titles
    ax[0].set_title("N-Less: 100ns")
    ax[1].set_title("N-Less: 1000ns")

def plot_diff():
    dmat_diff = dmat1 - dmat1000
    fig, ax = plt.subplots(figsize=(5,4))

    #pdiff = ax.pcolormesh(dmat_diff, cmap="bwr", vmin=-8, vmax=8)
    pdiff = ax.pcolormesh(dmat_diff, cmap="seismic")
    cbar = fig.colorbar(pdiff)
    cbar.set_label("∆ Distance ($\AA$)", labelpad=15)

    # xtick formatting
    ax.set_xticklabels(ctd_negs, rotation=45)
    ax.set_xticks([i + 0.5 for i in range(0, len(ctd_negs))])
    ax.set_xlabel("Residue Number")
    # ytick formattting
    ax.set_yticklabels(ntd_negs)
    ax.set_yticks([i + 0.5 for i in range(0, len(ntd_negs))])
    ax.set_ylabel("Residue Number")

    ax.set_title("N-Less: 100ns - 1000ns")
    #TODO: filter based on < 20 distances?

plot_1_v_1000()
plt.tight_layout()
#plt.savefig("figures/nless_compare100v1000_neg_dmat20.pdf")

#plot_diff()
# plt.savefig("figures/nless_100v1000diff_neg_dmat.pdf")

plt.show()