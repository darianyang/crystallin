import numpy as np
import matplotlib.pyplot as plt

dmat_path = "data/nalld/v01/1us"

dmat1 = np.loadtxt(f"{dmat_path}/negVnewasp_dmat100.dat")
dmat1000 = np.loadtxt(f"{dmat_path}/negVnewasp_dmat1000.dat")

asps = [24, 33, 49, 118, 124, 137, 160]
ntd_negs = [7, 8, 17, 21, 24, 33, 38, 46, 49, 61, 64, 73]
ctd_negs = [93, 95, 96, 103, 106, 107, 113, 118, 119, 124, 127, 134, 137, 149, 155, 160, 171]
all_negs = ntd_negs + ctd_negs

def plot_1_v_1000(): 
    gs_kw = dict(width_ratios=[1, 0.03])
    fig, ax = plt.subplots(ncols=2, nrows=3, figsize=(9,7), gridspec_kw=gs_kw)
    fig.subplots_adjust(wspace=0.3)
    p1 = ax[0,0].pcolormesh(dmat1, vmin=0, vmax=15)
    p1000 = ax[1,0].pcolormesh(dmat1000, vmin=0, vmax=15)
    cbar = fig.colorbar(p1, cax=ax[1,1])
    cbar.set_label("Distance ($\AA$)", labelpad=15)

    # labels
    fig.supxlabel("Asp & Glu Residue Number", x=0.48, y=0.03)
    fig.supylabel("Asn to Asp Residue Number", x=0.01, y=0.52)
    
    # filter based on < 20 distances?
    #dmat1[dmat1 > 20] = 0
    #dmat1000[dmat1000 > 20] = 0
    dmat_diff = dmat1 - dmat1000
    pdiff = ax[2,0].pcolormesh(dmat_diff, cmap="bwr", vmin=-10, vmax=10)
    #pdiff = ax[2,0].pcolormesh(dmat_diff, cmap="Reds", vmin=0, vmax=15)
    cbar2 = fig.colorbar(pdiff, cax=ax[2,1])
    cbar2.set_label("∆ Distance ($\AA$)", labelpad=15)

    # xtick formatting
    ax[0,0].set_xticklabels(all_negs, rotation=45)
    ax[0,0].set_xticks([i + 0.5 for i in range(0, len(all_negs))])
    ax[1,0].set_xticklabels(all_negs, rotation=45)
    ax[1,0].set_xticks([i + 0.5 for i in range(0, len(all_negs))])
    ax[2,0].set_xticklabels(all_negs, rotation=45)
    ax[2,0].set_xticks([i + 0.5 for i in range(0, len(all_negs))])

    # ytick formattting
    ax[0,0].set_yticklabels(asps)
    ax[0,0].set_yticks([i + 0.5 for i in range(0, len(asps))])
    ax[1,0].set_yticklabels(asps)
    ax[1,0].set_yticks([i + 0.5 for i in range(0, len(asps))])
    ax[2,0].set_yticklabels(asps)
    ax[2,0].set_yticks([i + 0.5 for i in range(0, len(asps))])

    # titles
    ax[0,0].set_title("N-Less: 100ns")
    ax[1,0].set_title("N-Less: 1000ns")
    ax[2,0].set_title("N-Less: 100ns - 1000ns")

    # get rid of unused axis
    ax[0,1].axis("off")


# def plot_diff():
#     # filter based on < 20 distances?
#     dmat1[dmat1 > 15] = 0
#     dmat1000[dmat1000 > 15] = 0
#     dmat_diff = dmat1 - dmat1000
#     fig, ax = plt.subplots(figsize=(5,4))

#     pdiff = ax.pcolormesh(dmat_diff, cmap="bwr", vmin=-8, vmax=8)
#     #pdiff = ax.pcolormesh(dmat_diff, cmap="seismic")
#     cbar = fig.colorbar(pdiff)
#     cbar.set_label("∆ Distance ($\AA$)", labelpad=15)

#     # xtick formatting
#     ax.set_xticklabels(all_negs, rotation=45)
#     ax.set_xticks([i + 0.5 for i in range(0, len(all_negs))])
#     ax.set_xlabel("Residue Number")
#     # ytick formattting
#     ax.set_yticklabels(asps)
#     ax.set_yticks([i + 0.5 for i in range(0, len(asps))])
#     ax.set_ylabel("Residue Number")

#     ax.set_title("N-Less: 100ns - 1000ns")

plot_1_v_1000()
plt.tight_layout()
#plt.savefig("figures/nless_compare100v1000_neg_dmat20.pdf")

#plot_diff()
# plt.savefig("figures/nless_100v1000diff_neg_dmat.pdf")

plt.savefig("figures/nless_negVnewasp_dmat2.pdf")
#plt.show()