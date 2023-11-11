""" Parsing CSV file with doses """
import pandas as pd

def parse_doses(file):
    """Parse coordiantes and doses to pamdas.DataFrame object

    :param file: CSV-file with ';' as delimiter and columns following convention that:
        first is longitude, second is latitude, third is dose rate. Coordinates is expected
        in EPSG:4326 CRS. Dose rate is expected in μSv/h.
    :returns: pandas.DataFrame object with contents of input file

    """
    df = pd.read_csv(file, sep=";")
    df.longitude = df.columns[0]
    df.latitude = df.columns[1]
    df.doses = df.columns[2]
    return df
