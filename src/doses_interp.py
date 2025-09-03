"""Interpolating dose data"""

from scipy.interpolate import LinearNDInterpolator
import numpy as np
import pandas as pd


def interpolate_doses(df):
    """Interpolate doses from dataframe and return new dataframe

    :param df: pandas.DataFrame with doses to interpolate, must contain longitude, latitude
        and doses columns.
    :returns: pandas.DataFrame with interpolated doses

    """
    lon = df[df.longitude]
    lat = df[df.latitude]
    doses = df[df.doses]

    interp = LinearNDInterpolator(list(zip(lon, lat)), doses)

    lon_lin = np.linspace(min(lon), max(lon), 1000)
    lat_lin = np.linspace(min(lat), max(lat), 1000)
    lon_grid, lat_grid = np.meshgrid(lon_lin, lat_lin)

    interp_df = pd.DataFrame()
    interp_df[df.longitude] = lon_grid.flatten()
    interp_df[df.latitude] = lat_grid.flatten()
    interp_df[df.doses] = interp(lon_grid, lat_grid).flatten()
    interp_df.longitude = df.longitude
    interp_df.latitude = df.latitude
    interp_df.doses = df.doses

    return interp_df
