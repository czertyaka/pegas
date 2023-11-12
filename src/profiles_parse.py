""" Parsing CSV file with profiles """
import pandas as pd


def parse_profiles(file):
    """Parse CSV file with profiles to pandas.DataFrame object

    :param file: CSV-file with ';' as delimiter and columns following convention that:
        first is longitude of first point;
        second is latitude of first point;
        third is longitude of second point;
        fourth is latitude of second point.
        Coordinates is expected in EPSG:4326 CRS.
    :returns: pandas.DataFrame object with contents of input file
    """
    df = pd.read_csv(file, sep=";")
    df.lon_first = df.columns[0]
    df.lat_first = df.columns[1]
    df.lon_second = df.columns[2]
    df.lat_second = df.columns[3]
    return df
