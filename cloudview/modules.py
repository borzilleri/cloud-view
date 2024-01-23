from . import firefox, safari, tot, home
from .datasource import DataSource
from typing import List

__sources: List[DataSource] = []


def render():
    data = [s.render() for s in __sources if s.enabled]
    return [section for section in data if section is not None]


def terminate():
    for s in __sources:
        s.stop()


def init(config: dict):
    section_conf = config.get("section", {})
    __sources.append(home.init(section_conf.get("home", {})))
    __sources.append(safari.init(section_conf.get("safari", {})))
    __sources.append(firefox.init(section_conf.get("firefox", {})))
    __sources.append(tot.init(section_conf.get("tot", {})))
    for s in __sources:
        s.start()
