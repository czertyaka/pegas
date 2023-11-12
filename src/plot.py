""" Pegas plotting facilities """

from math import floor, ceil, log10
import matplotlib.pyplot as plt
from matplotlib import colormaps, colors, cm
import geopandas as gpd
import contextily as cx


def create_plot():
    """Create figure to put axes on

    :returns: tuple of matplotlib.figure.Figure and matplotlib.axes.Axes
    """
    return plt.subplots(figsize=[8.3, 6])


def plot_doses(df, axes, fig):
    """Create axes and plot dose rates on it

    :param df: geopandas.GeoDataFrame with dose rates
    :param axes: matplotlib.axes.Axes to plot dose rates on
    :param fig: matplotlib.figure.Figure to plot colorbar on
    """
    cmap = colormaps["jet"]
    dosesIndex = df.columns[0]
    vmin = pow(10, floor(log10(df[dosesIndex].min())))
    vmax = pow(10, ceil(log10(df[dosesIndex].max())))
    norm = colors.LogNorm(vmin, vmax)
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=axes, label=dosesIndex)
    df.plot(column=dosesIndex, ax=axes, norm=norm, cmap=cmap, markersize=14)


def plot_basemap(axes, crs):
    """Plot background map

    :param axes: matplotlib.axes.Axes to plot backround map on
    :param crs: CRS in string format
    """
    cx.add_basemap(ax=axes, crs=crs, attribution="")


def plot_profiles(gs, axes):
    """Plot profiles

    :param gs: geopandas.GeoSeries with profiles
    :param axes: matplotlib.axes.Axes to plot profiles on
    """
    gs.plot(ax=axes, color="black")
