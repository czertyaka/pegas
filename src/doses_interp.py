"""Interpolating dose data"""

from scipy.interpolate import LinearNDInterpolator
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter


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

    interp_df = gauss_doses(interp_df)
    return interp_df


def gauss_doses(df):
    pv = pd.pivot_table(df, index=df.latitude, columns=df.longitude, values=df.doses)
    doses = pv.to_numpy()
    doses = np.log(doses)
    doses = gaussian_filter(doses, sigma=8, mode="nearest")
    doses = np.exp(doses)
    pv[:] = doses
    blurred_df = pv.melt(value_name=df.doses, ignore_index=False)
    blurred_df = blurred_df.reset_index()
    blurred_df.doses = df.doses
    blurred_df.longitude = df.longitude
    blurred_df.latitude = df.latitude
    return blurred_df
