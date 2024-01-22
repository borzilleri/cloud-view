from . import firefox, safari, tot, home

__sections = {
    "weather": home.render,
    "firefox": firefox.render,
    "safari": safari.render,
    "tot": tot.render,
}


def render_sections(config: dict):
    data = [
        __sections[name](conf)
        for (name, conf) in config.get("section", {}).items()
        if name in __sections and conf.get("enabled", False)
    ]
    return [section for section in data if section is not None]
