
import mdap
import matplotlib.pyplot as plt

plt.style.use("/Users/darian/github/wedap/wedap/styles/default.mplstyle")

# make input list for mdap
hhdist_files = [f"v{i:02d}/1us/hh_dist.dat" for i in range(0, 25)]
oa_files = [f"v{i:02d}/1us/o_angle.dat" for i in range(0, 25)]
rms_files = [f"v{i:02d}/1us/rmsd_bb.dat" for i in range(0, 25)]

mdap.MD_Plot(Xname=hhdist_files, Yname=rms_files, 
             plot_mode="hist", data_type="pdist").plot()

plt.xlabel("His-His Distance ($\AA$)")
plt.ylabel("Backbone RMSD ($\AA$)")
plt.tight_layout()
plt.show()
