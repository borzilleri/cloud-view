from . import cache, util
from .datasource import DataSource
import threading
from typing import Optional

__C_SHORTCUT = "shortcut-name"
__C_TIMEOUT = "cache-timeout"
__DEFAULT_TIMEOUT = 60


def __load_dots(shortcut_name: str) -> list[dict]:
    print("tot: querying dot info")
    dots = util.run_shortcut(shortcut_name)
    if not dots:
        print("tot: no data found.")
        return []
    for dot in dots:
        dot["lines"] = len(dot["text"].split("\n"))
    return dots


def __get_dots(config: dict, force: bool = False):
    if __C_SHORTCUT not in config:
        util.warn("tot: shortcut name not configured.")
        return None
    timeout = config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    return cache.get("tot", timeout, lambda: __load_dots(config[__C_SHORTCUT]), force)


def __render(config: dict) -> Optional[dict]:
    dots = __get_dots(config)
    if dots:
        return {"tpl": util.template("tot"), "data": {"dots": dots}}


def __update(config: dict):
    __get_dots(config, True)


def init(config: dict):
    return DataSource(
        config, __render, __update, config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    )
