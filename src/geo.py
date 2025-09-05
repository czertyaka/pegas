"""Convert regular data frames to geo data frames"""

from shapely.geometry import LineString
import pandas as pd
import geopandas as gpd


def create_doses_gdf(df):
    """Create geo data frame from data frame with dose rates

    :param: pandas.DataFrame with dose rates
    :returns: geopandas.GeoDataFrame with dose rates
    """
    gdf = gpd.GeoDataFrame(
        df[df.doses] if hasattr(df, "labels") is False else df[[df.doses, df.labels]],
        geometry=gpd.points_from_xy(df[df.longitude], df[df.latitude]),
        crs=4326,
    )
    gdf.doses = df.doses
    if hasattr(df, "labels"):
        gdf.labels = df.labels
    return gdf


def create_profiles_gs(df):
    """Create geo series from data frame with profiles coordinates

    :param: pandas.DataFrame with profiles coordinates
    :returns: geopandas.GeoSeries with profiles geometry
    """
    gs = gpd.GeoSeries(crs=4326)
    for _, row in df.iterrows():
        line = LineString(
            [
                [row[df.lon_first], row[df.lat_first]],
                [row[df.lon_second], row[df.lat_second]],
            ]
        )
        gs = pd.concat([gs, gpd.GeoSeries(line, crs=4326)])
    return gs


def create_clip_polygon(clip_file):
    """Create polygon for data clipping from GeoJson file

    :param file: GeoJson file with at least one polygon
    :returns: GeoDataFrame with polygon
    """
    gdf = gpd.read_file(clip_file)
    gdf = gdf.to_crs(epsg=4326)
    if len(gdf) == 0:
        raise ValueError(f"GeoJson file {clip_file} empty")
    poly = gdf.iloc[0]
    if poly.geometry.geom_type != "Polygon":
        raise ValueError(
            f"GeoJson file {clip_file} does not have " "polygon as its first entry"
        )
    return gdf


def clip_doses(doses_gdf, clip_polygon):
    """Clip doses in GeoDataFrame by custom Polygon

    :param doses_gdf: GeoDataFrame with doses to clip
    :param clip_polygon: GeoSeries with Polygon to clip by
    :returns: New GeoDataFrame with doses
    """
    assert doses_gdf.crs == clip_polygon.crs
    gdf = gpd.clip(doses_gdf, clip_polygon)
    gdf.doses = doses_gdf.doses
    return gdf
