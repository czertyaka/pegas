""" Pegas main script """

import matplotlib.pyplot as plt
from src.cli_args import args_parser
from src.doses_parse import parse_doses
from src.doses_interp import interpolate_doses
from src.profiles_parse import parse_profiles
from src.geo import create_doses_gdf, create_profiles_gs, create_clip_polygon, clip_doses
from src.plot import create_plot, plot_doses, plot_basemap, plot_profiles, plot_doses_heatmap


def main():
    """Pegas script entry point"""
    args = args_parser.parse_args()
    doses_df = parse_doses(args.doses_file)
    if args.plot_type == "heatmap":
        doses_df = interpolate_doses(doses_df)
    args.doses_file.close()
    doses_gdf = create_doses_gdf(doses_df)
    fig, axes = create_plot(doses_gdf.total_bounds)
    plot_basemap(axes, doses_gdf.crs.to_string())
    if args.clip_file is not None:
        clip_polygon = create_clip_polygon(args.clip_file)
        doses_gdf = clip_doses(doses_gdf, clip_polygon)
    if args.plot_type == "scatter":
        plot_doses(doses_gdf, axes, fig)
    elif args.plot_type == "heatmap":
        plot_doses_heatmap(doses_gdf, axes, fig)
    axes.set_xlabel(doses_df.longitude)
    axes.set_ylabel(doses_df.latitude)
    if args.profiles_file is not None:
        profiles_df = parse_profiles(args.profiles_file)
        args.profiles_file.close()
        profiles_gs = create_profiles_gs(profiles_df)
        plot_profiles(profiles_gs, axes)
    if args.plot_file is not None:
        plt.savefig(args.plot_file, bbox_inches="tight", dpi=600)
        args.plot_file.close()
    else:
        plt.show()


if __name__ == "__main__":
    main()
