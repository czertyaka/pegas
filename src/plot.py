""" Pegas plotting facilities """

from math import floor, ceil, log10
import matplotlib.pyplot as plt
from matplotlib import colormaps, colors, cm
import matplotlib.patheffects as pe
from adjustText import adjust_text
import contextily as cx
import osmnx as ox


def create_plot(bounds):
    """Create figure to put axes on

    :param bounds: box of xmin, ymin, xmax, ymax
    :returns: tuple of matplotlib.figure.Figure and matplotlib.axes.Axes
    """
    ratio = (bounds[2] - bounds[0])/(bounds[3] - bounds[1])
    figsize=[10*ratio, 10]
    fig, axes = plt.subplots(figsize=figsize)
    axes.set_ylim(bottom=bounds[1], top=bounds[3])
    axes.set_xlim(left=bounds[0], right=bounds[2])
    return (fig, axes)


def plot_doses(df, axes, fig):
    """Create axes and plot dose rates on it

    :param df: geopandas.GeoDataFrame with dose rates
    :param axes: matplotlib.axes.Axes to plot dose rates on
    :param fig: matplotlib.figure.Figure to plot colorbar on
    """
    cmap = colormaps["jet"]
    doses_index = df.columns[0]
    vmin = pow(10, floor(log10(df[doses_index].min())))
    vmax = pow(10, ceil(log10(df[doses_index].max())))
    norm = colors.LogNorm(vmin, vmax)
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=axes, label=doses_index)
    df.plot(column=doses_index, ax=axes, norm=norm, cmap=cmap, markersize=14)


def annotate_objects(axes):
    """Add objects annotations to a plot

    :param axes: matplotlib.axes.Axes to annotate objects on
    """
    south = axes.get_ylim()[0]
    north = axes.get_ylim()[1]
    west = axes.get_xlim()[0]
    east = axes.get_xlim()[1]
    gdf = ox.features.features_from_bbox(
        north=north, south=south, east=east, west=west, tags={"water": True}
    )
    gdf = gdf.drop_duplicates(subset="name")
    gdf = gdf.to_crs(epsg=2263)
    gdf["centroid"] = gdf.centroid.to_crs(epsg=4326)
    gdf = gdf.to_crs(epsg=4326)
    annotations = []
    for _, row in gdf.iterrows():
        if row["name"] != row["name"]:
            continue
        annotation = axes.annotate(
            row["name"],
            (row["centroid"].x, row["centroid"].y),
            zorder=1,
            annotation_clip=True,
            clip_on=True,
            ha="center",
            c="teal",
            wrap=True,
            fontsize=8,
            path_effects=[pe.withStroke(linewidth=2, foreground="white")],
        )
        annotations.append(annotation)
    adjust_text(texts=annotations, avoid_self=False, ax=axes, ensure_inside_axes=False)


def plot_basemap(axes, crs):
    """Plot background map

    :param axes: matplotlib.axes.Axes to plot backround map on
    :param crs: CRS in string format
    """
    cx.add_basemap(ax=axes, crs=crs, attribution="")
    annotate_objects(axes)


def plot_profiles(gs, axes):
    """Plot profiles

    :param gs: geopandas.GeoSeries with profiles
    :param axes: matplotlib.axes.Axes to plot profiles on
    """
    gs.plot(ax=axes, color="black")
