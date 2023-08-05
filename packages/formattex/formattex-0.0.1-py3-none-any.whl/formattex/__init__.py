import argparse
from pathlib import Path

from .intermediate_repr import create_internal_repr_texfile


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("files", nargs="+", help="src files to be formatted.")

    parser.add_argument(
        "--fast",
        type=bool,
        default=True,
        help="If --fast given, skip temporary sanity checks.",
    )

    parser.add_argument(
        "-l",
        "--line-length",
        type=int,
        default=87,
        help="How many characters per line to allow. [default: 87]",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose mode",
    )

    parser.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="Inplace mode (warning!)",
    )

    args = parser.parse_args()
    print(args)

    for path_input in args.files:
        repr = create_internal_repr_texfile(path_input, verbose=args.verbose)

        if args.verbose:
            print(repr.things)

        repr.dump(check=True)

        if args.inplace:
            path_output = path_input
        else:
            path_output = Path(path_input).with_name("tmp_formatted.tex")

        repr.save_formatted(path_output, line_length=args.line_length)
