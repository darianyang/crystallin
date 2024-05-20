
import mdap
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

plt.style.use("gdc.mplstyle")

fig, axes = plt.subplots(nrows=5, ncols=5, sharex=True, sharey=True, figsize=(8,8))

system = "wt"
system = "nallDd"

plot_options = {"plot_mode" : "scatter3d",
                "data_type" : "pdist",
                "cbar_label" : "Time (ns)",
                "scatter_interval" : 1,
                "scatter_s" : 1,
                "xlim" : (0, 6.5),
                "ylim" : (-2, 37),
                #"xlabel" : "Backbone RMSD (Å)" ,
                #"ylabel" : "Orientation Angle (°)" ,
                }

for v, ax in enumerate(tqdm(axes.reshape(-1))):
    rms = f"data/{system}/v{v:02d}/1us/rmsd_bb.dat"
    oa = f"data/{system}/v{v:02d}/1us/o_angle.dat"
    mdp = mdap.MD_Plot(Xname=rms, Yname=oa, Zname=oa, Zindex=0, ax=ax, **plot_options)
    mdp.plot(cbar=False)
    ax.set_xticks([0, 3, 6])
    ax.set_xticklabels([0, 3, 6])
    ax.set_yticks([0, 15, 30])
    ax.set_yticklabels([0, 15, 30])

#fig.suptitle("WT $\gamma$-D-Crystallin", x=0.54, y=0.96)
#fig.suptitle("N-Less $\gamma$-D-Crystallin", x=0.54, y=0.96)
#fig.suptitle("L-Asp $\gamma$-D-Crystallin", x=0.54, y=0.96)
fig.suptitle("D-Asp $\gamma$-D-Crystallin", x=0.54, y=0.96)
#fig.suptitle("L-iso-Asp $\gamma$-D-Crystallin", x=0.54, y=0.96)
#fig.suptitle("D-iso-Asp $\gamma$-D-Crystallin", x=0.54, y=0.96)
fig.supxlabel("Backbone RMSD (Å)", x=0.56, y=0.035)
fig.supylabel("Orientation Angle (°)")
plt.tight_layout()
#plt.show()
plt.savefig(f"figures/{system}_25scatter.pdf")
    
