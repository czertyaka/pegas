""" Pegas main script """

from src.cli_args import args_parser
from src.doses_parse import parse_doses

def main():
    """ Pegas script entry point """
    args = args_parser.parse_args()
    doses_df = parse_doses(args.doses_file)
    print(doses_df[doses_df.doses].describe())

if __name__ == "__main__":
    main()
