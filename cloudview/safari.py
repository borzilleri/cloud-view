from . import cache, util
from .datasource import DataSource
import sqlite3
import tempfile
import uuid
from pathlib import Path
from typing import Optional

__C_CLOUDTABS = "cloudtabs"
__C_TIMEOUT = "cache-timeout"
__DEFAULT_TIMEOUT = 20

__QUERY = "SELECT t.title, t.url, d.device_name from cloud_tabs t JOIN cloud_tab_devices d on t.device_uuid == d.device_uuid;"


def __load_data(db_file: str):
    print("safari: querying CloudTabs.db")
    db_path = str(Path(db_file).expanduser().absolute())
    temp_db = f"{tempfile.gettempdir()}/{str(uuid.uuid4())}"
    result = {}
    try:
        # We copy the database into a temp file, to avoid some
        # access/permissions and also ensure we're not interfering with
        # normal safari/icloud operations.
        util.run_cmd(f"cp '{db_path}' '{temp_db}'")
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        for row in cursor.execute(__QUERY):
            (title, url, device) = row
            if device not in result:
                result[device] = []
            result[device].append({"title": title, "url": url})
    except sqlite3.OperationalError as ex:
        util.warn(f"safari: sqlite error: {ex}")
    finally:
        # Remove our temp file when we're finished.
        Path(temp_db).unlink()
    return result


def __get_safari_tabs(config: dict, force: bool = False):
    if __C_CLOUDTABS not in config:
        util.warn("safari: CloudTabs.db path not configured.")
        return None
    timeout = config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    return cache.get(
        "safari", timeout, lambda: __load_data(config[__C_CLOUDTABS]), force
    )


def __render(config: dict) -> Optional[dict]:
    return util.tpl_include(
        "browser",
        {
            "browser": config["name"],
            "devices": __get_safari_tabs(config, not config.get("cache-enabled", True)),
        },
    )


def __update(config: dict):
    __get_safari_tabs(config, True)


def init(config: dict):
    return DataSource(
        config, __render, __update, config.get(__C_TIMEOUT, __DEFAULT_TIMEOUT)
    )
