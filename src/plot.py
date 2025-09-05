"""Pegas plotting facilities"""

from math import floor, ceil, log10
import matplotlib.pyplot as plt
from matplotlib import colormaps, colors, cm
import matplotlib.patheffects as pe
from adjustText import adjust_text
import contextily as cx
import osmnx as ox
import pandas as pd
import numpy as np


def mouse_event(event):
    print(f"{event.xdata};{event.ydata}")


def create_plot(bounds):
    """Create figure to put axes on

    :param bounds: box of xmin, ymin, xmax, ymax
    :returns: tuple of matplotlib.figure.Figure and matplotlib.axes.Axes
    """
    ratio = (bounds[2] - bounds[0]) / (bounds[3] - bounds[1])
    figsize = [10 * ratio, 10]
    fig, axes = plt.subplots(figsize=figsize)
    y_margin = (bounds[3] - bounds[1]) / 20
    x_margin = (bounds[2] - bounds[0]) / 20
    axes.set_ylim(bottom=bounds[1] - y_margin, top=bounds[3] + y_margin)
    axes.set_xlim(left=bounds[0] - x_margin, right=bounds[2] + x_margin)
    fig.canvas.mpl_connect("button_press_event", mouse_event)
    return (fig, axes)


def plot_doses(df, axes, fig):
    """Create axes and plot dose rates on it

    :param df: geopandas.GeoDataFrame with dose rates
    :param axes: matplotlib.axes.Axes to plot dose rates on
    :param fig: matplotlib.figure.Figure to plot colorbar on
    """
    cmap = colormaps["jet"]
    doses_index = df.doses
    vmin = pow(10, floor(log10(df[doses_index].min())))
    vmax = pow(10, ceil(log10(df[doses_index].max())))
    norm = colors.LogNorm(vmin, vmax)
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=axes, label=doses_index)
    # df.plot(column=doses_index, ax=axes, norm=norm, cmap=cmap, markersize=50, edgecolor="black")
    df.plot(column=doses_index, ax=axes, norm=norm, cmap=cmap, markersize=14)
    if not hasattr(df, "labels"):
        return
    annotations = []
    for _, row in df.iterrows():
        annotation = axes.annotate(
            row[df.labels],
            (row.geometry.x, row.geometry.y),
            ha="center",
            fontsize=8,
            path_effects=[pe.withStroke(linewidth=2, foreground="white")],
        )
        annotations.append(annotation)
    adjust_text(texts=annotations, ax=axes)


def plot_doses_heatmap(df, axes, fig):
    cmap = colormaps["YlOrRd"]
    doses_index = df.doses
    vmin = pow(10, floor(log10(df[doses_index].min())))
    vmax = pow(10, ceil(log10(df[doses_index].max())))
    norm = colors.LogNorm(vmin, vmax)
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=axes, label=doses_index)

    df["x"] = df.geometry.x
    df["y"] = df.geometry.y

    pv = pd.pivot_table(df, index="y", columns="x", values=df.doses)
    x = pv.columns.values
    y = pv.index.values
    doses = pv.values

    axes.pcolormesh(x, y, doses, cmap=cmap, norm=norm)

    _, ymin, _, ymax = df.total_bounds
    df_y = (ymax + ymin) / 2
    aspect = 1 / np.cos(np.radians(df_y))
    axes.set_aspect(aspect)


def annotate_objects(axes):
    """Add objects annotations to a plot

    :param axes: matplotlib.axes.Axes to annotate objects on
    """
    bottom = axes.get_ylim()[0]
    top = axes.get_ylim()[1]
    left = axes.get_xlim()[0]
    right = axes.get_xlim()[1]
    gdf = ox.features.features_from_bbox(
        bbox=(left, bottom, right, top), tags={"water": "lake"}
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
    # adjust_text(texts=annotations, avoid_self=False, ax=axes, ensure_inside_axes=False)


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
    gs.plot(ax=axes, color="black", linestyle="--", linewidth=1)


def plot_clip_borders(df, axes):
    """Plot clip border

    :param df: geopandas.GeoDataFrame with clip polygon
    :param axes: matplotlib.axes.Axes to plot profiles on
    """
    df.plot(ax=axes, linewidth=1, edgecolor="black", facecolor="none")
