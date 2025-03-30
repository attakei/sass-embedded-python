import os
import sys
import subprocess
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

RELEASE_TARGET = {
    "win_amd64": {"os": "windows", "arch": "x64"},
    "win_arm64": {"os": "windows", "arch": "arm64"},
    "manylinux_2_17_x86_64": {"os": "linux", "arch": "x64"},
    "manylinux_2_17_aarch64": {"os": "linux", "arch": "arm64"},
}

here = Path(__file__).parent


class CustomHook(BuildHookInterface):
    def initialize(self, version, build_data):
        if "BUILD_FOR_PLATFORM" not in os.environ:
            return
        if os.environ["BUILD_FOR_PLATFORM"] not in RELEASE_TARGET:
            return
        platform = os.environ["BUILD_FOR_PLATFORM"]
        release = RELEASE_TARGET[platform]

        build_data["pure_python"] = False
        py_tag = "py3"
        abi_tag = "none"
        build_data["tag"] = f"{py_tag}-{abi_tag}-{platform}"
        cmd = f"python -m sass_embedded.dart_sass --clean --os {release['os']} --arch {release['arch']}"
        subprocess.run(cmd.split(), cwd=here / "src")
