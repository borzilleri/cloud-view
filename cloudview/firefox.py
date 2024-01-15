from . import util
import json
import time
from typing import Optional

__C_FFSCLIENT = "ffsclient"
__C_TIMEOUT = "cache-timeout"
__DEFAULT_TIMEOUT = 10
__CACHE = {"data": None, "ts": 0}


def __load_ffsync_data(ffsclient_exe: str) -> dict[str, dict]:
    print("firefox: querying sync client.")
    data = util.run_cmd(f"{ffsclient_exe} tabs list --format json")
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
    timeout = config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    now = int(time.time())
    if not __CACHE["data"] or now > (__CACHE["ts"] + timeout):
        if __C_FFSCLIENT in config:
            data = __load_ffsync_data(config[__C_FFSCLIENT])
            if data:
                __CACHE["data"] = data
                __CACHE["ts"] = now
        else:
            util.warn("firefox: ffsclient path not configured.")
    else:
        print("firefox: loading cached data.")
    return __CACHE["data"]


def render(config: dict) -> Optional[dict]:
    tabs = __get_ff_tabs(config)
    if tabs:
        return util.tpl_include("browser", {"browser": config["name"], "devices": tabs})
