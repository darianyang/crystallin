"""
Code written for 03702 final project.
"""

import numpy as np
from matplotlib import pyplot as plt
import MDAnalysis as mda

def traj_loader(parm, crd, step=1000):
    """
    Load and return a trajectory from mda universe.
    Input parmater file, coordinate file, and loading step interval (default=1000).
    """
    traj = mda.Universe(parm, crd, in_memory=True, in_memory_step=step, verbose=True)
    return traj

def rog_calc(universe):
    """
    Returns a ndarray of RoG values for each timestep in trajectory.
    """
    RoG = []
    protein = universe.select_atoms("protein")
    for step in universe.trajectory:
        RoG.append(protein.radius_of_gyration())
    return np.array(RoG)

# load WT traj, stepsize 1000 should = 20 frames
wt = traj_loader("1hk0_wt/200ns/1hk0_200ns_dry.prmtop", "1hk0_wt/200ns/1hk0_200ns_10i_dry.ncdf")
n33d = traj_loader("1hk0_n33d/200ns/1hk0_n33d_200ns_dry.prmtop", "1hk0_n33d/200ns/1hk0_n33d_200ns_10i_dry.ncdf")
rog_data = [rog_calc(wt), rog_calc(n33d)]

# # make boxplot
# plt.boxplot(rog_data, labels=["WT", "N33D"])
# plt.ylabel("Radius of Gyration (Å)")
# plt.xlabel("Simulation Set")
# plt.savefig("figures/rog_200ns.png", dpi=300)


#----------------------------------------------------------------------------#
# Part 2: Normal probability plots (quantile vs. quantile plot)
import scipy.stats as stats

# 1 row, 2 col, go to plot 1
# plt.subplot(1, 2, 1)
# ls_fit_wt = stats.probplot(rog_calc(wt), dist="norm", plot=plt)
# plt.title("WT")
# print("WT", ls_fit_wt)

# # go to plot 2
# plt.subplot(1, 2, 2)
# ls_fit_n33d = stats.probplot(rog_calc(n33d), dist="norm", plot=plt)
# plt.title("N33D")
# print("N33D", ls_fit_n33d)

# plt.tight_layout()
# #plt.show()
# plt.savefig("figures/norm_prob.png", dpi=300)


#----------------------------------------------------------------------------#
# Part 3: statistical testing
def f_test(x, y):
    x = np.array(x)
    y = np.array(y)
    f = np.var(x, ddof=1) / np.var(y, ddof=1) # calculate F test statistic 
    dfn = x.size - 1 # define degrees of freedom numerator 
    dfd = y.size - 1 # define degrees of freedom denominator 
    p = 1 - stats.f.cdf(f, dfn, dfd) # find p-value of F test statistic 
    return f, p

# perform F-test: returns F statistic and p-value
#print(f_test(rog_calc(wt), rog_calc(n33d)))

# perform t-test: returns T statistic and p-value
#print(stats.ttest_ind(rog_calc(wt), rog_calc(n33d)))


#----------------------------------------------------------------------------#
# Part 4: PCA
from MDAnalysis.analysis import pca, align

def pca_cv(universe, num_pcs=10):
    """
    Allign and run pca on a universe trajectory object.
    """
    aligner = align.AlignTraj(universe, universe, select='backbone',
                            in_memory=True).run()

    pc = pca.PCA(wt, select='backbone',
                align=False, mean=None, # traj pre-aligned, no mean ref structure
                n_components=num_pcs).run() # save first n PCs
    return pc

wt_pc = pca_cv(wt)
n33d_pc = pca_cv(n33d)

# # 1 row, 2 col, go to plot 1
# plt.subplot(1, 2, 1)
# plt.plot(wt_pc.cumulated_variance[:10])
# plt.xlabel('Principal Component')
# plt.ylabel('Cumulative Variance')
# plt.title("WT")

# # 1 row, 2 col, go to plot 2
# plt.subplot(1, 2, 2)
# plt.plot(n33d_pc.cumulated_variance[:10])
# plt.xlabel('Principal Component')
# plt.ylabel('Cumulative Variance')
# plt.title("N33D")

# plt.tight_layout()
# plt.show()
# plt.savefig("figures/pca_cv.png", dpi=300)