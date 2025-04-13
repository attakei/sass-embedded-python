"""Example for sending Protobuf message into Dart Sass process (embedded mode)."""

import time
from textwrap import dedent

from sass_embedded.protocol.compiler import Host
from sass_embedded.protocol.embedded_sass_pb2 import InboundMessage


def walk_version_request(host: Host):
    """Communicate to fetch version information."""
    req = InboundMessage()
    req.version_request.id = 0
    resp = host.send_message(req)
    print(f"Compiler version: {resp.version_response.compiler_version}")
    print(f"Protocol version: {resp.version_response.protocol_version}")


def walk_compile_string(host: Host):
    """Communicate to compile SCSS source into CSS string."""
    req = InboundMessage()
    req.compile_request.string.source = dedent(
        """
$font-stack: Helvetica, sans-serif;
$primary-color: #333;

body {
  font: 100% $font-stack;
  color: $primary-color;
}
    """.strip()
    )
    resp = host.send_message(req)
    print(resp.compile_response.success.css)
    print(resp.compile_response.success.source_map)


def main():
    # Pre: set up host process.
    host = Host()
    host.connect()
    # Post/Get version information
    print("=== Showing version information.")
    walk_version_request(host)
    time.sleep(2)
    print("=== Compile source.")
    walk_compile_string(host)
    time.sleep(2)
    # Post: Finish host process.
    host.close()


if __name__ == "__main__":
    main()
