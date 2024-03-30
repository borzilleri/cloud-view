from . import cache, util
from .datasource import DataSource
import json
from typing import Optional

__C_FFSCLIENT = "ffsclient"
__C_TIMEOUT = "cache-timeout"
__DEFAULT_TIMEOUT = 10


def __load_data(ffsclient_exe: str) -> dict[str, dict]:
    print("firefox: querying sync client.")
    data = util.run_cmd(
        f"{ffsclient_exe} tabs list --force-refresh-session --format json --minimized-json"
    )
    result = {}
    if data:
        tabs = json.loads(data)
        for t in tabs:
            client = t["client_name"]
            if client not in result:
                result[client] = []
            result[client].append({"title": t["title"], "url": t["urlHistory"][0]})
    else:
        print("firefox: no data found.")
    return result


def __get_ff_tabs(config: dict, force: bool = False):
    if __C_FFSCLIENT not in config:
        util.warn("firefox: ffsclient path not configured.")
        return None
    timeout = config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    return cache.get(
        "firefox", timeout, lambda: __load_data(config[__C_FFSCLIENT]), force
    )


def __render(config: dict) -> Optional[dict]:
    return util.tpl_include(
        "browser",
        {
            "browser": config["name"],
            "devices": __get_ff_tabs(config, config.get("cache-enabled", True)),
        },
    )


def __update(config: dict):
    __get_ff_tabs(config, True)


def init(config: dict):
    return DataSource(
        config, __render, __update, config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    )
