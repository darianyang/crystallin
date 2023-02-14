"""
Plotting functions for rmsd and rmsf with uncertainties.
"""

import numpy as np
import matplotlib
import matplotlib.patches 
from matplotlib import pyplot as plt
import matplotlib.patheffects as path_effects


# TODO: add functionality for dynamic y columns?
# TODO: add class (OOP) and init functionality (learning exercise)
    # TODO: then reformat using OOP oriented matplotlib style
    # call axes methods: fig, ax = plt.subplots()
    # ax.set_xticks(loc), etc.

def rmsd_format():
    """
    RMSD plot formatting.
    """
    plt.figure()

    # TODO: add custom axis ticks and limits
    plt.xlabel("Time (us)")
    plt.ylabel("Backbone Heavy Atom RMSD ($\AA$)")
    #plt.yticks(np.arange(0, 5.25, 1.0))
    #plt.ylim(0, 5)

def rmsf_format():
    """
    RMSF plot formatting.
    """
    plt.figure()
    plt.xlabel("Residue Number")
    plt.xticks(np.arange(0,177,88))
    plt.xlim(0,180)
    plt.ylabel("RMSF ($\AA$)")

    mono_resno = 88
    helix_elements = {6:10, 17:30, 35:50, 54:63, 67:75}

    # highlight secondary elements
    for key, value in helix_elements.items():
        plt.axvspan(key, value, color="red", alpha=0.20)
        plt.axvspan(key + mono_resno, value + mono_resno, color="red", alpha=0.20)

    # for formatting legend
    plt.axvspan(0, 0, color="red", alpha=0.25, label=r"$Helix$")
    
    plt.text(25, -0.25, "(CA CTD Monomer 1)", fontsize=9)
    plt.text(115, -0.25, "(CA CTD Monomer 2)", fontsize=9)


def xy_plot(target_file, color, style, alpha=1, \
    savefig=None, data_label=None, linewidth=None, x_unit=None, legend=None):
    """
    Simple X Y plot of 2 column data.
    Style can be in "line", "scatter", "step".
    """
    data = np.genfromtxt(target_file)
    x = data[:, :1]
    y = data[:, 1:2]

    if x_unit == "nano" or x_unit == "ns":
        # convert ps to ns
        x = np.divide(x, 1000)
    elif x_unit == "micro" or x_unit == "us":
        # convert ps to us
        x = np.divide(x, 1000000)

    if style == "line":
        plt.plot(x, y, \
            linewidth=linewidth, color=color, label=data_label, alpha=alpha, linestyle='solid')
    elif style == "scatter":
        plt.scatter(x, y, \
            markersize=8, color=color, label=data_label, alpha=alpha, markerstyle='circle')
    elif style == "step":
            plt.step(x, y, \
            linewidth=linewidth, color=color, label=data_label, alpha=alpha, linestyle='solid')
 
    if legend != None:
        plt.legend(loc=legend)

    plt.tight_layout()

    if savefig is not None:
        plt.savefig(savefig, dpi=300)


# plot all 5 rmsd traj on one plot
# rmsd_format()
# colors = ["placeholder", "black", "red", "lime", "indigo", "teal"]
# for i in range(1,6):
#     xy_plot(f"m0{i}/m0{i}_2kod_1us_10i.rms", colors[i], "line", alpha=0.75, \
#         x_unit="ns", legend=None, linewidth=0.2, data_label=f"2KOD m0{i}")

# #plt.show()
# plt.savefig("figures/m01-05_1us_rmsd.png", dpi=300)

#------------------------------------------------------------------------#
# plot 1hk0 backbone rmsd
time = "200ns"
version = "v01"
rmsd_format()
xy_plot(f"1hk0_wt/{version}/{time}/1hk0_{time}.rms", "k", "line", alpha=0.75,
        x_unit="us", legend=None, linewidth=0.2, data_label=f"1hk0 WT")
# xy_plot(f"1hk0_n33d/{version}/{time}/1hk0_n33d_{time}.rms", "cornflowerblue", "line", alpha=0.75,
#         x_unit="us", legend=None, linewidth=0.2, data_label=f"1hk0 N33D")

plt.legend(loc=2)
plt.show()
#plt.savefig("figures/m01_monomers_nofit_rmsd.png", dpi=300)


def data_format_fill_between(data_root_name, start_iter, end_iter, x_unit=None, frame_norm=None):
    """
    Take multiple sets of X,Y data and generate list of 5 arrays.
    X must be conserved, multi-Y average +/- stdev populate Y1,Y2 columns.
    Y3 is avgerages, Y4 is stdevs.
    """

    # list of multiple arrays
    multi_y = []

    # loop and load in each dataset as an ndarray
    for i in range(start_iter, end_iter + 1):

        data = np.genfromtxt(f"m0{i}/" + f"m0{i}_" + data_root_name, dtype=float)

        x = data[:, :1]
        y = data[:, 1:2]
        multi_y.append(y)

    if x_unit == "nano" or x_unit == "ns":
        # convert ps to ns
        x = np.divide(x, 1000)

    # avg and stdev ndarrays from multiple y arrays
    avg = np.average(multi_y[:100000], axis=0)
    stdev = np.std(multi_y[:100000], axis=0)  

    # final columns/arrays in list
    fill_between_data = []
    fill_between_data.append(np.concatenate(x, axis=0))
    fill_between_data.append(np.concatenate(np.add(avg, stdev), axis=0))
    fill_between_data.append(np.concatenate(np.subtract(avg, stdev), axis=0))
    fill_between_data.append(np.concatenate(avg, axis=0))
    fill_between_data.append(np.concatenate(stdev, axis=0))

    return fill_between_data

""" # get average rmsf data, save as new file
fill_data = data_format_fill_between("res_rmsf.dat", 1, 5)
rmsf_data = open("avg_rmsf.dat", "w")
for i in range(0,176):
    rmsf_data.write(f"{fill_data[0][i]}\t{fill_data[3][i]}\n")
rmsf_data.close()
"""

def plot_uncertainty(data, stdev=False, savefig=None, step=None):
    """
    Plot a fill.between() style X Y graph to represent multiple Y datasets.
    Input is list with 5 lists: X, Ymax, Ymin, averages, stdevs.
    """
    plt.fill_between(data[0], data[1], data[2], \
        step=step, color="cornflowerblue", alpha=0.5, label=r"$Avg \pm \sigma$")

    if step == None:
        plt.plot(data[0], data[3], \
        color="cornflowerblue", linewidth=0.8, label=r"$Average$")
    else:
        plt.step(data[0], data[3], \
        color="cornflowerblue", linewidth=0.8, label=r"$Average$")

    if stdev is True:
        plt.plot(data[0], data[4], \
        color="k", linewidth=0.8, label=r"$Stdev$")

    plt.legend(loc=2)
    plt.tight_layout()

    if savefig is not None:
        plt.savefig(savefig, dpi=300)



#fill_data = data_format_fill_between("res_rmsf.dat", 1, 5)
#rmsf_format()
#plot_uncertainty(fill_data, step="pre", savefig="figures/m01-05_rmsf.png", stdev=False)


# fill_data = data_format_fill_between("2kod_1us_10i.rms", 1, 5, x_unit="us")
# rmsd_format()
# plot_uncertainty(fill_data, savefig="figures/m01-05_avg_rmsd_1us.png")

# plt.show()


# plot m01 rmsf step plot only
#rmsf_format()
#xy_plot("m01/m01_res_rmsf.dat", "cornflowerblue", "step", \
#    data_label="2KOD m01", legend=2, savefig="figures/m01_rmsf.png")