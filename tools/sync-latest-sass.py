#!/usr/bin/env python
from pathlib import Path

import yaml

from sass_embedded import _const as const

root = Path(__file__).parents[1]


def pick_sass_version(aqua: dict):
    for pkg in aqua["packages"]:
        if pkg["name"].startswith("sass/dart-sass@"):
            return pkg["name"].split("@")[1]
    raise Exception("Package is not found")


def main():
    aqua_yaml_path = root / "aqua.yaml"
    aqua = yaml.safe_load(aqua_yaml_path.read_text())
    sass_version = pick_sass_version(aqua)
    print(f"- Current version: {const.DART_SASS_VERSION}")
    print(f"- Loaded version:  {sass_version}")
    if sass_version == const.DART_SASS_VERSION:
        return 0
    print("Detect newer Dart Sass.")
    pass


if __name__ == "__main__":
    main()
