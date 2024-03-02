import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

__root = Path(__file__).parent
__tpl = __root / "templates"
__assets = __root / "assets"


def warn(s: str):
    print(s, file=sys.stderr)


def run_shortcut(name, debug: bool = False):
    out = run_cmd(f"shortcuts run '{name}'", debug)
    if out:
        return json.loads(out)
    return None


def run_cmd(cmd: str, debug: bool = False) -> Optional[str]:
    if debug:
        print(cmd)
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if debug:
        print(out)
    if out.returncode != 0:
        warn(out.stderr)
    elif out.stdout and len(out.stdout) > 0:
        return out.stdout.strip()
    return None


def template(name: str):
    tpl_path = __tpl / f"{name}.html"
    return str(tpl_path)

def assets_dir() -> str:
    return str(__assets)


def tpl_include(name: str, data) -> dict:
    return {"tpl": template(name), "data": data}
