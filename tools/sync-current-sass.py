#!/usr/bin/env python
import re
from pathlib import Path

import yaml

from sass_embedded import _const as const

root = Path(__file__).parents[1]

TARGETS = {
    root / "src/sass_embedded/_const.py": [
        {
            "match": r'DART_SASS_VERSION = ".+"',
            "replace": r'DART_SASS_VERSION = "{version}"',
        }
    ],
    root / ".age.toml": [
        {
            "match": r":Dart Sass version: .+",
            "replace": r":Dart Sass version: {version}",
        }
    ],
}


def pick_sass_version(aqua: dict):
    for pkg in aqua["packages"]:
        if pkg["name"].startswith("sass/dart-sass@"):
            return pkg["name"].split("@")[1]
    raise Exception("Package is not found")


def update_sources(version: str):
    for src, rules in TARGETS.items():
        lines = src.read_text().split("\n")
        new_lines = []
        for idx, line in enumerate(lines):
            if not line:
                new_lines.append(line)
                continue
            for rule in rules:
                if not re.fullmatch(rule["match"], line):
                    continue
                line = rule["replace"].format(version=version)
            else:
                new_lines.append(line)
        src.write_text("\n".join(new_lines))


def main():
    aqua_yaml_path = root / "aqua.yaml"
    aqua = yaml.safe_load(aqua_yaml_path.read_text())
    sass_version = pick_sass_version(aqua)
    print(f"- Current version: {const.DART_SASS_VERSION}")
    print(f"- Loaded version:  {sass_version}")
    if sass_version == const.DART_SASS_VERSION:
        return 0
    print("Detect newer Dart Sass.")
    update_sources(sass_version)
    pass


if __name__ == "__main__":
    main()
