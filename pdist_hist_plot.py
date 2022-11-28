"""
Process and plot a heatmap of 2 datasets from standard MD simulations.
"""

import numpy as np
import matplotlib.pyplot as plt

# Suppress divide-by-zero in log
np.seterr(divide='ignore', invalid='ignore')

# TODO: clean this up and make it more robust, combine with simple data plot script

#plt.rcParams['figure.figsize']= (10,6)
plt.rcParams.update({'font.size': 14})
plt.rcParams["font.family"]="Sans-serif"
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['mathtext.default'] = 'regular'
plt.rcParams['axes.linewidth'] = 2.5
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['xtick.major.width'] = 2.5
plt.rcParams['xtick.minor.size'] = 2
plt.rcParams['xtick.minor.width'] = 2
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['ytick.major.width'] = 2.5

def pre_processing(x_files, y_files, x_loc=1, y_loc=1):
    """
    Parameters
    ----------
    x_files : list of str
        One or multiple dataset paths - 2D array with aux value at each frame.
    y_files : list of str
        One or multiple dataset paths - 2D array with aux value at each frame.
    x_loc : int
        Index of the X ndarray column for the target aux data.
    y_loc : int
        Index of the Y ndarray column for the target aux data.

    Returns
    -------
    X : ndarray
    Y : ndarray
    Z : ndarray
    """
    X = np.concatenate([np.genfromtxt(i)[:,x_loc] for i in x_files])
    Y = np.concatenate([np.genfromtxt(i)[:,y_loc] for i in y_files])
 
    # get rid of nan values: return array without (not) True nan values
    X = X[np.logical_not(np.isnan(X))]
    Y = Y[np.logical_not(np.isnan(Y))]

    # numpy equivalent to: ax.hist2d(c2[:,1], aux)
    hist, x_edges, y_edges = np.histogram2d(X, Y, bins=100)
    # let each row list bins with common y range
    hist = np.transpose(hist)
    # convert histogram counts to pdist (-ln(P(x)))
    hist = -np.log(hist / np.max(hist))
    # get bin midpoints
    midpoints_x = (x_edges[:-1] + x_edges[1:]) / 2
    midpoints_y = (y_edges[:-1] + y_edges[1:]) / 2

    return midpoints_x, midpoints_y, hist

def pdist_plot(X, Y, Z, pmax=5, pmin=0, plot_style="heat", ax=None, cmap="afmhot", savefig=None, **plot_options):
    """
    Parameters
    ----------
    X : ndarray
        1D array of midpoints for histogram data.
    Y : ndarray
        1D array of midpoints for histogram data.
    Z : ndarray
        2D array of the histogram values.
    pmax : int
        Max probability (Z) value.
    pmin : int
        Min probability (Z) value.
    plot_style : str
        'heat', or 'contour'
    ax : mpl axes object
    cmap : str
        mpl colormap string.
    savefig : str
        Path to optionally save the figure output.
    **plot_options : kwargs

    # TODO: add option to plot KDE of hist.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5,4))
    else:
        fig = plt.gca()

    if plot_style == "heat": # TODO: add contour lines
        plot = ax.pcolormesh(X, Y, Z, cmap=cmap, shading="auto", vmin=pmin, vmax=pmax)
    elif plot_style == "contour":
        levels = np.arange(pmin, pmax + 1, 1)
        lines = ax.contour(X, Y, Z, levels=levels, colors="black", linewidths=1)
        plot = ax.contourf(X, Y, Z, levels=levels, cmap=cmap)

   # unpack plot options dictionary
    for key, item in plot_options.items():
        if key == "xlabel":
            ax.set_xlabel(item, weight="bold")
        if key == "ylabel":
            ax.set_ylabel(item, weight="bold")
        if key == "xlim":
            ax.set_xlim(item)
        if key == "ylim":
            ax.set_ylim(item)
        if key == "xticks":
            ax.set_xticks(item)
        if key == "xtick_labels":
            ax.set_xticklabels(item)
        if key == "yticks":
            ax.set_yticks(item)
        if key == "ytick_labels":
            ax.set_yticklabels(item)
        if key == "title":
            ax.set_title(item, fontweight="bold", fontsize=14, pad=12)
        if key == "grid":
            ax.grid(item, alpha=0.5)

    cbar = fig.colorbar(plot)
    #cbar.set_label(r"$\left[-\ln\,P(x)\right]$")
    #cbar.set_label(r"$\Delta F(\vec{x})\,/\,kT$" + "\n" + r"$\left[-\ln\,P(x)\right]$")
    # TODO: add lines

    #fig.tight_layout()
    if savefig:
        fig.savefig(savefig, dpi=300, transparent=True)
    else:
        plt.show()

    return plot

datanamex = "rmsd_bb.dat"
datanamey = "o_angle.dat"
x_files = [f"data/wt/v{i:02d}/1us/{datanamex}" for i in range(0,5)]
y_files = [f"data/nalld/v{i:02d}/1us/{datanamey}" for i in range(0,5)]
X, Y, Z = pre_processing(x_files, y_files)
pdist_plot(X, Y, Z, pmax=5, plot_style="contour")