from . import cloudview
import argparse
import sys
from typing import Optional

def __init_args(argv: Optional[list] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", help="Specify a config file to load.",
        default="config.toml"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port to run the server on."
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> Optional[int]:
    args = __init_args(argv)
    cloudview.start(args)
    return 0

if __name__ == "__main__":
    retval = main()
    sys.exit(retval)