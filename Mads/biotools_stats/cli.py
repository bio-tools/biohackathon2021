"""
The command line tool for the biotools_statistics package

"""
import sys
from argparse import ArgumentParser, FileType, Namespace


class CustomArgumentParser(ArgumentParser):
    """
    The custom argument parser, which prints the help on error.
    """

    def error(self, message: str):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        exit(2)


def _create_argument_parser() -> CustomArgumentParser:
    """
    Create the argument parser.

    :return: The argument parser.
    """
    parser: CustomArgumentParser = CustomArgumentParser(description="Command-line tool for calculating the statistics "
                                                                    "for bio.tools for a given set of tools.")

    return parser


def main():
    """
    The main entry point.
    """
    parser: CustomArgumentParser = _create_argument_parser()
    args: Namespace = parser.parse_args()


if __name__ == "__main__":
    main()
