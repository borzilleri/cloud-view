from . import modules, util
import argparse
import tomllib
from pathlib import Path
from bottle import route, run, template

__CONFIG = {}


@route("/")
def index():
    return template(
        util.template("index"),
        sections=modules.render_sections(__CONFIG),
    )


def __load_config(path: str):
    global __CONFIG
    config_path = Path(path)
    if config_path.is_file():
        with config_path.open("rb") as f:
            __CONFIG = tomllib.load(f)


def start(args: argparse.Namespace):
    __load_config(args.config)
    run(host="localhost", port=args.port, debug=args.debug)
