""" Pegas CLI arguments parsing """
import argparse

args_parser = argparse.ArgumentParser(
    prog="pegas",
    description="""PEdestrian GAmma Survey (pegas) is designed to plot pedestrian gamma-ray survey
    results.""",
)
args_parser.add_argument(
    "-d",
    "--doses-file",
    help="""CSV file path with cooridnates and dose rates""",
    required=True,
    type=argparse.FileType("r"),
    dest="doses_file",
)
args_parser.add_argument(
    "-pr",
    "--profiles-file",
    help="""CSV file path with profiles coordinates""",
    required=False,
    type=argparse.FileType("r"),
    dest="profiles_file",
)
args_parser.add_argument(
    "-c",
    "--clip-file",
    help="""Geojson file with single polygon to clip shown data""",
    required=False,
    type=argparse.FileType("r"),
    dest="clip_file",
)
args_parser.add_argument(
    "-t",
    "--plot-type",
    help="""Plot type (default: scatter)""",
    choices=["scatter", "heatmap"],
    default="scatter",
    required=False,
    type=str,
    dest="plot_type"
)
args_parser.add_argument(
    "-o",
    "--output",
    help="""Output image file path, open image if not given""",
    required=False,
    type=argparse.FileType("wb"),
    dest="plot_file",
)
