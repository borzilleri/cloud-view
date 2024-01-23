from . import modules, util
import argparse
import signal
import sys
import tomllib
from pathlib import Path
from bottle import route, run, template


def handle_signal(signal, frame):
    modules.terminate()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


@route("/")
def index():
    return template(
        util.template("index"),
        sections=modules.render(),
    )


def __load_config(path: str) -> dict:
    config_path = Path(path)
    if config_path.is_file():
        with config_path.open("rb") as f:
            return tomllib.load(f)
    return {}


def start(args: argparse.Namespace):
    config = __load_config(args.config)
    modules.init(config)
    run(host="localhost", port=args.port, debug=args.debug)
