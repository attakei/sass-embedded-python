"""Process manager of Dart Sass Compiler."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import TYPE_CHECKING

from blackboxprotobuf.lib.types import varint

from ..dart_sass import Release
from .embedded_sass_pb2 import OutboundMessage

if TYPE_CHECKING:
    from typing import Optional

    from ..dart_sass import Executable
    from .embedded_sass_pb2 import InboundMessage


@dataclass
class Packet:
    """Packet component to send process.

    This has attributes and procedure to send ``InboundMessage`` for host process.

    :ref: https://github.com/sass/sass/blob/main/spec/embedded-protocol.md#packet-structure
    """

    compilation_id: int
    message: InboundMessage

    def to_bytes(self) -> bytes:
        """Convert to bytes stream for Dart Sass."""
        msg = self.message.SerializeToString()
        id_bytes = varint.encode_varint(self.compilation_id)
        length = len(id_bytes + msg)
        len_bytes = varint.encode_varint(length)
        return bytes(len_bytes + id_bytes) + msg


class Host:
    """Host process of compiler."""

    executable: Executable
    _proc: Optional[subprocess.Popen]
    _id: int

    def __init__(self):
        self.executable = Release.init().get_executable()
        self._proc = None
        self._id = 1

    def __del__(self):
        self.close()

    def connect(self):
        """Open and connect Sass process."""
        if self._proc:
            return
        command = [
            self.executable.dart_vm_path,
            self.executable.sass_snapshot_path,
            "--embedded",
        ]
        self._proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            bufsize=0,
        )

    def close(self):
        """Stop host process."""
        if self._proc:
            self._proc.communicate()

    def make_packet(self, message: InboundMessage) -> Packet:
        """Convert from protobuf message to packet structure.

        :param message: Sending message.
        :returns: Packet component.
        """
        cid = 0 if message.WhichOneof("message") == "version_request" else self._id
        if cid:
            self._id += 1
        return Packet(compilation_id=cid, message=message)

    def send_message(self, message: InboundMessage) -> OutboundMessage:
        """Send protobuf message for host process.

        :param message: Sending message.
        :returns: Parsed protbuf message.
        """
        if not self._proc:
            raise Exception("Dart Sass process is not started.")
        # Sending packet.
        packet = self.make_packet(message)
        self._proc.stdin.write(packet.to_bytes())  # type: ignore[union-attr]
        # Recieve packet.
        out = b""
        idx = 0
        length = 0
        while not self._proc.stdout.closed:  # type: ignore[union-attr]
            out += self._proc.stdout.read(8)  # type: ignore[union-attr]
            if not out:
                continue
            length, idx = varint.decode_varint(out, 0)
            if length == len(out[idx:]):
                break
        # Parse packet.
        cid, cidx = varint.decode_varint(out, idx)
        if cid != packet.compilation_id:
            raise Exception("CompilationID of request and response are not matched.")
        msg = OutboundMessage()
        msg.ParseFromString(out[cidx:])
        return msg
