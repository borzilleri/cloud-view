from . import modules, util
import argparse
import signal
import sys
import tomllib
from pathlib import Path
from bottle import route, run, template, static_file


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

@route("/assets/<filepath:path>")
def img(filepath):
    return static_file(filepath, root=util.assets_dir())


def __load_config(path: str) -> dict:
    config_path = Path(path)
    if config_path.is_file():
        with config_path.open("rb") as f:
            return tomllib.load(f)
    return {}


def __run_server(conf: dict):
    run(
        host=conf.get("host", "localhost"),
        port=conf.get("port", 8080),
        debug=conf.get("debug", True),
    )


def start(args: argparse.Namespace):
    config = __load_config(args.config)
    modules.init(config)
    __run_server(config.get("server", {}))
