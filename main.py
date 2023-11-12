""" Pegas main script """

import matplotlib.pyplot as plt
from src.cli_args import args_parser
from src.doses_parse import parse_doses
from src.profiles_parse import parse_profiles
from src.geo import create_doses_gdf, create_profiles_gs
from src.plot import create_plot, plot_doses, plot_basemap, plot_profiles


def main():
    """Pegas script entry point"""
    args = args_parser.parse_args()
    doses_df = parse_doses(args.doses_file)
    doses_gdf = create_doses_gdf(doses_df)
    fig, ax = create_plot()
    plot_doses(doses_gdf, ax, fig)
    if args.profiles_file is not None:
        profiles_df = parse_profiles(args.profiles_file)
        profiles_gs = create_profiles_gs(profiles_df)
        plot_profiles(profiles_gs, ax)
    plot_basemap(ax, doses_gdf.crs.to_string())
    plt.show()


if __name__ == "__main__":
    main()
