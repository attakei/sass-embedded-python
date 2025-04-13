#!/usr/bin/env python
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.request import urlopen

PROTOCOL_FILE_URL = (
    "https://github.com/sass/sass/raw/refs/heads/main/spec/embedded_sass.proto"
)

root = Path(__file__).parent


def main() -> int:
    # Check exists protoc.
    if not shutil.which("protoc"):
        sys.stderr.write("Require protoc.\n")
        return 1
    # Fetch protocol file.
    resp = urlopen(PROTOCOL_FILE_URL)
    if resp.status != 200:
        sys.stderr.write("Failed to fetch protcol file.\n")
        return 1
    proto_dir = Path(tempfile.mkdtemp())
    proto_path = proto_dir / "embedded_sass.proto"
    proto_path.write_bytes(resp.read())
    command = [
        "protoc",
        f"--proto_path={proto_dir}",
        f"--python_out={root / 'src' / 'sass_embedded' / 'protocol'}",
        f"--pyi_out={root / 'src' / 'sass_embedded' / 'protocol'}",
        str(proto_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("Created!!")
        return 0
    sys.stderr.write(f"{result.stdout}\n\n{result.stderr}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
