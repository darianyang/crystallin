"""
Plot simple 1D timeseries data and KDE.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.patches 

import matplotlib.gridspec as gridspec
import scipy.stats

import pandas as pd

# plt.rcParams['figure.figsize']= (10,6)
plt.rcParams.update({'font.size': 16})
plt.rcParams["font.family"]="Sans-serif"
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['mathtext.default'] = 'regular'
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 6
plt.rcParams['xtick.minor.width'] = 2
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['axes.labelsize'] = 18

#plt.style.use("~/github/wedap/wedap/styles/default.mplstyle")

def pre_processing(file=None, data=None, time_units=10**6, index=1):
    """
    Processes raw time series data to appropriate units of time.
    """
    if file:
        data = np.genfromtxt(file)
    # time units should mostly be in ps: convert to us
    time = np.divide(data[:,0], time_units)
    return np.vstack([time, data[:,index]])

def avg_and_stdev(data_list, contacts=False):
    """
    Returns the average and stdev of multiple timeseries datasets.
    """
    # only the y values, x axis is time
    if contacts is True:
        data = [np.divide(i[1], i[1,0]) for i in data_list]
    else:
        data = [i[1] for i in data_list]
    return np.average(data, axis=0), np.std(data, axis=0)

def movingaverage(data, windowsize):
    """
    Returns the window averaged 1D dataset.
    """
    return np.convolve(data, np.ones(windowsize, dtype=float) / windowsize, mode='same')

def line_plot(time, data, ylim=(0,5), ax=None, stdev=None, alpha=0.8, window=1,
              label=None, leg_cols=5, color=None, ylabel=None, dist=(0,1.1,0.2), linewidth=1):
    """
    Parameters
    ----------
    time : array
        Timeseries values.
    data : array
        Dataset values.
    ylim : tuple
        2 item tuple to set custom y limits.
    stdev : array
        Used to generate errors for the line plot.
    label : str
        Label the line plot.
    leg_cols : int
        Number of columns in the legend.
    dist : tuple
        Fed into np.arange(dist) for dist plot x-axis ticks.

    Returns
    -------

    """
    if ax is None:
        fig, ax = plt.subplots(ncols=2, sharey=True, gridspec_kw={'width_ratios' : [20, 5]})
    else:
        fig = plt.gcf()

    if window != 1:
        time = time[window:-window:window]
        data = movingaverage(data, window)[window:-window:window]
        #print(data[window:-window])
        if stdev is not None:
            stdev = stdev[window:-window:window]

    # line plot
    ax[0].plot(time, data, linewidth=linewidth, alpha=alpha, label=label, color=color)
    #ax[0].axvline(2, color="k", lw=2, ls="--")
    ax[0].set_xlabel("Time ($\mu$s)", labelpad=12, fontweight="bold")
    #ax[0].set_ylabel(r"RMSD ($\AA$)", labelpad=10, fontweight="bold")
    #ax[0].set_ylabel(r"19F to C=O Distance ($\AA$)", labelpad=10, fontweight="bold")
    ax[0].set_ylabel(ylabel, labelpad=11, fontweight="bold")
    ax[0].set_ylim(ylim)
    #ax[0].set_xticks(np.arange(0, time[-1] + (time[-1] / 5), time[-1] / 5), minor=True)
    ax[0].grid(alpha=0.5)

    # secondary kde distribution plot
    grid = np.arange(ylim[0], ylim[1], .01, dtype=float)
    density = scipy.stats.gaussian_kde(data)(grid)
    ax[1].plot(density, grid, color=color)
    # TODO: maybe normalize density to 1 and then set xticks np.arange(0, 1, 0.2)
    ax[1].set_xticks(np.arange(dist[0], dist[1], dist[2]))
    #ax[1].set_xticks(np.arange(0, np.max(density) + 0.5, 0.5))
    ax[1].xaxis.set_ticklabels([])
    ax[1].set_xlabel("Distribution", labelpad=28, fontweight="bold")
    ax[1].grid(alpha=0.5)

    # optionally plot the stdev using fill_between
    if stdev is not None:
        ax[0].fill_between(time, np.add(data, stdev), np.subtract(data, stdev), alpha=0.25, color=color)
    if label:
        ax[0].legend(loc=8, frameon=False, ncol=leg_cols, bbox_to_anchor=(0.5, -0.38))

    #fig.tight_layout()
    #fig.savefig("figures/test.png", dpi=300, transparent=False)

def dist_plot(data, xlim=(0,5), ax=None, color=None, linewidth=3):
    """
    Plot just the distribution of R1 or R2 values.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = plt.gca()
    # secondary kde distribution plot
    grid = np.arange(xlim[0], xlim[1], .01, dtype=float)
    density = scipy.stats.gaussian_kde(data)(grid)
    ax.plot(grid, density, color=color, linewidth=linewidth)
    # TODO: maybe normalize density to 1 and then set xticks np.arange(0, 1, 0.2)
    #ax.set_xticks(np.arange(0, 1.2, 0.2))
    #ax.set_xticks(np.arange(0, np.max(density) + 0.5, 0.5))
    #ax.set_xlabel("Relaxation ($s^{-1}$)", labelpad=18, fontweight="bold")

    # Remove the non-bottom spines
    for kw in ("left", "right", "top"):
        ax.spines[kw].set_visible(False)
    ax.axes.yaxis.set_visible(False)

def add_patch(ax, recx, recy, facecolor, text, recwidth=0.04, recheight=0.06, recspace=0, fontsize=18):
    ax.add_patch(matplotlib.patches.Rectangle((recx, recy), 
                                                recwidth, recheight, 
                                                facecolor=facecolor,
                                                edgecolor='black',
                                                clip_on=False,
                                                transform=ax.transAxes,
                                                lw=2.25)
                    )
    ax.text(recx + recheight + recspace, recy + recheight / 2, text, ha='left', va='center',
            transform=ax.transAxes, fontsize=fontsize)

def plot_avg_and_stdev(dataname, ylim, ylabel, time_units=10**4, dist=(0,5,1), 
                       replicates=(0,3), savefig=None, contacts=False, linewidth=1):
    cmap = cm.tab10
    norm = Normalize(vmin=0, vmax=10)
    fig, ax = plt.subplots(ncols=2, sharey=True, gridspec_kw={'width_ratios' : [20, 5]})
    #for num, sys in enumerate(["wt", "n33d", "b3d", "nalld"]):
    for num, sys in enumerate(["wt", "nalld"]):
        color = cmap(norm(num))

        # all replicates of a res class
        res = [pre_processing(f"data/{sys}/v{i:02d}/1us/{dataname}", time_units=time_units) 
               for i in range(replicates[0], replicates[1])]
        # fix for fraction contacts
        if contacts is True:
            avg, stdev = avg_and_stdev(res, contacts=contacts)
        else:
            avg, stdev = avg_and_stdev(res)
        line_plot(res[0][0], avg, stdev=stdev, ax=ax, ylim=ylim, 
                  color=color, ylabel=ylabel, linewidth=linewidth,
                  alpha=0.85, dist=dist)
        
        # recx can be controlled as : left margin + spacing
        add_patch(ax[0], 0.02 + 0.265 * num, -0.435, color, f"{sys.upper()}", fontsize=16)

    ax[1].set_xlim(dist[0], dist[1])
    fig.tight_layout()
    if savefig:
        fig.savefig(f"figures/{savefig}", dpi=300, transparent=True)
    plt.show()

def plot_multiple_reps(dataname, ylim, ylabel, time_units=10**4, dist=(0,5,1), 
                       replicates=(0,3), savefig=None, contacts=False, window=1, linewidth=1):
    cmap = cm.tab10
    norm = Normalize(vmin=0, vmax=10)
    fig, ax = plt.subplots(ncols=2, sharey=True, gridspec_kw={'width_ratios' : [20, 5]})
    #for num, sys in enumerate(["wt", "n33d", "b3d", "nalld"]):
    labels = ["WT $\gamma$D-Crystallin", "N-less $\gamma$D-Crystallin"]
    for num, sys in enumerate(["wt", "nalld"]):
        color = cmap(norm(num))
        for rep in range(replicates[0], replicates[1]):
            # all replicates of a res class
            data = pre_processing(f"data/{sys}/v{rep:02d}/1us/{dataname}", time_units=time_units) 
            line_plot(data[0], data[1], ax=ax, ylim=ylim,
                      color=color, ylabel=ylabel, window=window,
                      alpha=0.85, dist=dist, linewidth=linewidth)
        
        # recx can be controlled as : left margin + spacing
        #add_patch(ax[0], 0.02 + 0.265 * num, -0.435, color, f"{sys.upper()}", fontsize=16)
        add_patch(ax[0], 0.152 + 0.365 * num, -0.435, color, labels[num], fontsize=16)

    ax[1].set_xlim(dist[0], dist[1])
    fig.tight_layout()
    if savefig:
        fig.savefig(f"figures/{savefig}", dpi=300, transparent=False)
    plt.show()

def multi_rep_data(sys="nalld", dataname="o_angle.dat", replicates=(0,25)):
    data = [pre_processing(f"data/{sys}/v{i:02d}/1us/{dataname}")[1] 
               for i in range(replicates[0],replicates[1])]
    data = np.reshape(data, -1)
    return data

# data and axis for dist and joint plots
# fig, ax = plt.subplots()
# wt = multi_rep_data("wt")
# nless = multi_rep_data("nalld")

# # dist plot
# xlim = (0,35)
# dist_plot(wt, xlim, ax=ax)
# dist_plot(nless, xlim, ax=ax)

def joint_plot1(gdc="wt"):
    # joint plot
    import seaborn as sns
    import pandas as pd
    replicates = (0,25)
    #replicates = (0,5)
    #replicates = (0,1)
    wt1 = multi_rep_data(gdc, "rmsd_bb.dat", replicates=replicates)
    wt2 = multi_rep_data(gdc, "o_angle.dat", replicates=replicates)
    wt_df = pd.DataFrame(np.vstack((wt1, wt2)))
    full_df = pd.concat([wt_df], axis=1, ignore_index=True)
    #print(np.shape(wt_df))
    full_df = full_df.T
    # set legend col for labeling
    full_df["Legend"] = ["WT" for i in range(0, np.shape(wt_df)[1])]
    #print(full_df)
    # space is for magin plot padding
    g = sns.JointGrid(x=0, y=1, data=full_df, hue="Legend", palette=["dimgrey"], space=0)
    g.plot_joint(sns.kdeplot, fill=False, common_norm=False, levels=8)
    g.plot_marginals(sns.kdeplot, fill=False, common_norm=False)
    #g.set_axis_labels(xlabel="Backbone RMSD ($\AA$)", ylabel="Orientation Angle (°)")
    g.ax_joint.set_xlabel("Backbone RMSD ($\AA$)", labelpad=9)
    g.ax_joint.set_ylabel("Orientation Angle (°)", labelpad=14)
    #sns.move_legend(g, "upper left", bbox_to_anchor=(.55, .45), title="")
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    # move the legend in ax_joint
    sns.move_legend(g.ax_joint, "upper right", title='', frameon=False)

def joint_plot(og_gdc="wt", alt_gdc="nalld", alt_gdc_label="L-Asp"):
    # joint plot
    import seaborn as sns
    import pandas as pd
    replicates = (0,25)
    #replicates = (0,5)
    #replicates = (0,1)
    wt1 = multi_rep_data(og_gdc, "rmsd_bb.dat", replicates=replicates)
    wt2 = multi_rep_data(og_gdc, "o_angle.dat", replicates=replicates)
    nless1 = multi_rep_data(alt_gdc, "rmsd_bb.dat", replicates=replicates)
    nless2 = multi_rep_data(alt_gdc, "o_angle.dat", replicates=replicates)
    wt_df = pd.DataFrame(np.vstack((wt1, wt2)))
    nless_df = pd.DataFrame(np.vstack((nless1, nless2)))
    full_df = pd.concat([wt_df, nless_df], axis=1, ignore_index=True)
    #print(np.shape(wt_df))
    full_df = full_df.T
    # set legend col for labeling
    full_df["Legend"] = ["WT" for i in range(0, np.shape(wt_df)[1])] + \
                        [alt_gdc_label for i in range(0, np.shape(nless_df)[1])]
    #print(full_df)
    # space is for magin plot padding
    g = sns.JointGrid(x=0, y=1, data=full_df, hue="Legend", palette=["dimgrey", "magenta"], space=0)
    g.plot_joint(sns.kdeplot, fill=False, common_norm=False, levels=8)
    g.plot_marginals(sns.kdeplot, fill=False, common_norm=False)
    #g.set_axis_labels(xlabel="Backbone RMSD ($\AA$)", ylabel="Orientation Angle (°)")
    g.ax_joint.set_xlabel("Backbone RMSD ($\AA$)", labelpad=9)
    g.ax_joint.set_ylabel("Orientation Angle (°)", labelpad=14)
    #sns.move_legend(g, "upper left", bbox_to_anchor=(.55, .45), title="")
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    # move the legend in ax_joint
    sns.move_legend(g.ax_joint, "upper right", title='', frameon=False)

# RoG
#plot_avg_and_stdev("radgyr.dat", (15.5,18.5), "RoG ($\AA$)", replicates=(1,2))

# Backbone RMSD
#plot_avg_and_stdev("rmsd_bb.dat", (0,7), "Backbone RMSD ($\AA$)", replicates=(0,5), time_units=10**3)
# plot_multiple_reps("rmsd_bb.dat", (0,6), "Backbone RMSD ($\AA$)", replicates=(0,5), 
#                     window=10, time_units=10**3, linewidth=2)

# nc and nnc (TODO: index)
#plot_avg_and_stdev("nc_number.dat", (0.7,1.1), "Fraction of Contacts", replicates=(1,2), contacts=True)
#res = pre_processing(f"data/wt/v00/1us/nc_number.dat", time_units=10**3)
#line_plot(res[0,:], np.divide(res[1,:],res[1,0]), ylim=(0.8,1.1), alpha=0.85)
#plt.show()

# angle and dist of domains
# plot_multiple_reps("domain_angle.dat", (60,90), "Domain Angle (°)", replicates=(0,5), 
#                     window=10, time_units=10**3, linewidth=2)

# plot_multiple_reps("domain_distance.dat", (24,30), "Domain Distance ($\AA$)", replicates=(0,5), 
#                     window=10, time_units=10**3, linewidth=2)

# ntd an ctd rmsd
# plot_multiple_reps("rmsd_bb_ntd.dat", (0,20), "NTD RMSD ($\AA$)", replicates=(0,5), 
#                     window=10, time_units=10**3, linewidth=2)
# plot_multiple_reps("rmsd_bb_ctd.dat", (0,20), "CTD RMSD ($\AA$)", replicates=(0,5), 
#                     window=10, time_units=10**3, linewidth=2)

# plot orientation angleq
# plot_multiple_reps("o_angle.dat", (0,35), "Orientation Angle (°)", replicates=(0,5), 
#                     window=10, time_units=10**3, linewidth=2, dist=(0,0.2,0.02))

joint_plot1()
plt.savefig("figures/joint_25us_wt_only.png", dpi=300, transparent=True)
plt.show()

#joint_plot(og_gdc="nallD", alt_gdc="nallDd", alt_gdc_label="D-Asp")
#joint_plot(alt_gdc="nallDd", alt_gdc_label="D-Asp")
#plt.savefig("figures/joint_5us_wt_d-Nless.png", dpi=300, transparent=True)
#plt.savefig("figures/joint_25us_wt_d-Nless.png", dpi=300, transparent=True)
#plt.show()

#joint_plot()
#plt.savefig("figures/joint_25us_wt_l-Nless.png", dpi=300, transparent=True)
#plt.show()

#joint_plot(alt_gdc="allb3d", alt_gdc_label="L-iso-Asp")
#plt.savefig("figures/joint_25us_wt_allLb3d.png", dpi=300, transparent=True)
#plt.show()

#joint_plot(alt_gdc="allDb3d", alt_gdc_label="D-iso-Asp")
#plt.savefig("figures/joint_25us_wt_allDb3d.png", dpi=300, transparent=True)
#plt.show()
