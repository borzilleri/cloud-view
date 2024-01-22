from . import cache, util
import json
from typing import Optional

__C_FFSCLIENT = "ffsclient"
__C_TIMEOUT = "cache-timeout"
__DEFAULT_TIMEOUT = 10


def __load_ffsync_data(ffsclient_exe: str) -> dict[str, dict]:
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


def __get_ff_tabs(config: dict):
    if __C_FFSCLIENT not in config:
        util.warn("firefox: ffsclient path not configured.")
        return None
    timeout = config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    return cache.get(
        "firefox", timeout, lambda: __load_ffsync_data(config[__C_FFSCLIENT])
    )


def render(config: dict) -> Optional[dict]:
    return util.tpl_include(
        "browser", {"browser": config["name"], "devices": __get_ff_tabs(config)}
    )
