import subprocess
import sys
from pathlib import Path
from typing import Optional

__tpl = Path(__file__).parent / "templates"


def warn(s: str):
    print(s, file=sys.stderr)


def run_cmd(cmd: str) -> Optional[str]:
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if out.returncode != 0:
        warn(out.stderr)
    elif out.stdout and len(out.stdout) > 0:
        return out.stdout.strip()
    return None


def template(name: str):
    tpl_path = __tpl / f"{name}.html"
    return str(tpl_path)


def tpl_include(name: str, data) -> dict:
    return {"tpl": template(name), "data": data}
