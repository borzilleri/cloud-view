from . import cache, util
from .datasource import DataSource
from typing import Optional

__C_SHORTCUT = "shortcut"
__C_TIMEOUT = "cache-timeout"
__DEFAULT_TIMEOUT = 300
__DEFAULT_TEMP = "F"


"""
{
    "bedroom": {
        "temp": "17.2°C",
        "humidity": "35",
        "aqi": "36.6 μg/m³",
        "airquality": "1",
    },
    "den": {
        "temp": "22°C",
        "humidity": "32",
    },
    "livingroom": {
        "temp": "19.7°C",
        "humidity": "35"
    }
}
"""


def __c_to_f(c: float) -> str:
    f = int(((c * 9) / 5) + 32)
    return f"{f}°F"


def __f_to_c(f: float) -> str:
    c = round((f - 32) * (5 / 9), 2)
    return f"{c}°C"


def __parse_temp(val, target_scale) -> str:
    scale = val[-1]
    if scale == target_scale:
        return val
    t = float(val[:-2])
    if scale == "C" and target_scale == "F":
        return __c_to_f(t)
    elif scale == "F" and target_scale == "C":
        return __f_to_c(t)
    else:
        return "??"


def __parse_humidity(val) -> str:
    return f"{val}%"


def __parse_aqi(val) -> str:
    "36.6 μg/m³"
    return val


def __parse_metric(metric, val, config) -> Optional[dict]:
    if metric == "temp":
        return {
            "name": "Temp",
            "value": __parse_temp(val, config.get("temperature", __DEFAULT_TEMP)),
        }
    if metric == "humidity":
        return {"name": "Humidity", "value": __parse_humidity(val)}


def __load_data(shortcut_name):
    print("home: querying weather data")
    data = util.run_shortcut(shortcut_name)
    if not data:
        print("home: no weather data found.")
        return {}
    return data


def __parse_data(config: dict, data: dict):
    result = []
    for room, name in config.get("rooms", {}).items():
        room_data = {"name": name, "metrics": []}
        for metric, val in data.get(room, {}).items():
            metric_data = __parse_metric(metric, val, config)
            if metric_data:
                room_data["metrics"].append(metric_data)
        if room_data["metrics"]:
            result.append(room_data)
    return result


def __get_weather(config: dict, force: bool = False):
    timeout = config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    if __C_SHORTCUT not in config:
        util.warn("home: weather shortcut name not configured.")
        return None
    return cache.get(
        "weather", timeout, lambda: __load_data(config[__C_SHORTCUT]), force
    )


def __update(config: dict):
    __get_weather(config, True)


def __render(config: dict) -> Optional[dict]:
    data = __get_weather(config)
    if not data:
        return None
    rooms = __parse_data(config, data)
    if rooms:
        return {"tpl": util.template("home"), "data": {"rooms": rooms}}


def init(config: dict):
    return DataSource(
        config, __render, __update, config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    )
