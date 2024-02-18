from . import cloudview
import argparse
import sys
from typing import Optional


def __init_args(argv: Optional[list] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", help="Specify a config file to load.", default="config.toml"
    )
    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> Optional[int]:
    args = __init_args(argv)
    cloudview.start(args)
    return 0


if __name__ == "__main__":
    retval = main()
    sys.exit(retval)
