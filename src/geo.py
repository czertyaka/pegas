""" Convert regular data frames to geo data frames """

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
