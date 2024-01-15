from . import firefox, safari, tot, util
import argparse
import tomllib
from pathlib import Path
from bottle import route, run, template

__CONFIG = {}


@route("/")
def index():
    sections = []
    if __CONFIG["firefox"]["enabled"]:
        data = firefox.render(__CONFIG["firefox"])
        if data:
            sections.append(data)
    if __CONFIG["safari"]["enabled"]:
        data = safari.render(__CONFIG["safari"])
        if data:
            sections.append(data)
    if __CONFIG["tot"]["enabled"]:
        data = tot.render(__CONFIG["tot"])
        if data:
            sections.append(data)
    return template(util.template("index"), sections=sections)


def __load_config(path: str):
    global __CONFIG
    config_path = Path(path)
    if config_path.is_file():
        with config_path.open("rb") as f:
            __CONFIG = tomllib.load(f)


def start(args: argparse.Namespace):
    __load_config(args.config)
    run(host="localhost", port=args.port, debug=args.debug)
