#!/usr/bin/python3

"""
scan a music directory to find concerts near a specified location
"""

from .version import __version__
from .cli import parse_args
from .scan import scan_wrapper
from .concerts import bit
from .output import output_wrapper


def main():
    """Main function."""
    args = parse_args()
    raw_artists = scan_wrapper(args.directory, args.cache)
    concert_list = bit(raw_artists, args)
    output_wrapper(concert_list, args.output)


if __name__ == "__main__":
    main()
