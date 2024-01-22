from . import util
import json
import time
from typing import Optional

__C_SHORTCUT = "shortcut-name"
__C_TIMEOUT = "cache-timeout"
__DEFAULT_TIMEOUT = 20

__CACHE = {"data": None, "ts": 0}


def __load_dots(shortcut_name: str) -> list[dict]:
    print("tot: querying dot info")
    dots = util.run_shortcut(shortcut_name)
    if not dots:
        print("tot: no data found.")
        return []
    for dot in dots:
        dot["lines"] = len(dot["text"].split("\n"))
    return dots


def __get_dots(config: dict):
    timeout = config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    now = int(time.time())
    if not __CACHE["data"] or now > (__CACHE["ts"] + timeout):
        if __C_SHORTCUT in config:
            data = __load_dots(config[__C_SHORTCUT])
            if data:
                __CACHE["data"] = data
                __CACHE["ts"] = now
        else:
            util.warn("tot: shortcut name not configured.")
    else:
        print("tot: loading cached data")
    return __CACHE["data"]


def render(config: dict) -> Optional[dict]:
    dots = __get_dots(config)
    if dots:
        return {"tpl": util.template("tot"), "data": {"dots": dots}}
