
import numpy as np
import matplotlib.pyplot as plt

dmat_path = "data/nalld/v01/1us"

dmat1 = np.loadtxt(f"{dmat_path}/newASP_dmat100.dat")
dmat1000 = np.loadtxt(f"{dmat_path}/newASP_dmat1000.dat")

asps = [24, 33, 49, 118, 124, 137, 160]

def plot_1_v_1000(): 
    gs_kw = dict(width_ratios=[1, 1, 0.06])
    fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(8,4), gridspec_kw=gs_kw)
    fig.subplots_adjust(wspace=0.3)
    p1 = ax[0].pcolormesh(dmat1, vmin=0, vmax=20)
    p1000 = ax[1].pcolormesh(dmat1000, vmin=0, vmax=20)
    cbar = fig.colorbar(p1, cax=ax[2])
    cbar.set_label("Distance ($\AA$)", labelpad=15)
    fig.supxlabel("Asp Residue Number", x=0.48, y=0.04, fontsize=11)
    fig.supylabel("Asp Residue Number", x=0.01, y=0.55, fontsize=11)
    
    # xtick formatting
    ax[0].set_xticklabels(asps)
    ax[0].set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    ax[1].set_xticklabels(asps)
    ax[1].set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])

    # ytick formattting
    ax[0].set_yticklabels(asps)
    ax[0].set_yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    ax[1].set_yticklabels([])
    ax[1].set_yticks([])

    # titles
    ax[0].set_title("N-Less: 100ns")
    ax[1].set_title("N-Less: 1000ns")

def plot_diff():
    # filter based on < 20 distances?
    # dmat1[dmat1 > 20] = 0
    # dmat1000[dmat1000 > 20] = 0
    dmat_diff = dmat1 - dmat1000
    fig, ax = plt.subplots(figsize=(5,4))

    pdiff = ax.pcolormesh(dmat_diff, cmap="bwr", vmin=-8, vmax=8)
    #pdiff = ax.pcolormesh(dmat_diff, cmap="seismic", vmin=-8, vmax=8)
    cbar = fig.colorbar(pdiff)
    cbar.set_label("∆ Distance ($\AA$)", labelpad=15)

    # xtick formatting
    ax.set_xticklabels(asps)
    ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    ax.set_xlabel("Asp Residue Number")
    # ytick formattting
    ax.set_yticklabels(asps)
    ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    ax.set_ylabel("Asp Residue Number")

    ax.set_title("N-Less: 100ns - 1000ns")

plot_1_v_1000()
plt.tight_layout()
plt.savefig("figures/nless_compare100v1000_asp_dmat20_2.pdf")

plot_diff()
plt.savefig("figures/nless_100v1000diff_asp_dmat_2.pdf")

plt.show()