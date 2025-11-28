"""Process manager of Dart Sass Compiler."""

from __future__ import annotations

import subprocess
import asyncio

from pathlib import Path
from dataclasses import dataclass
from typing import TYPE_CHECKING

from blackboxprotobuf.lib.types import varint
from textwrap import dedent

import logging

from ..dart_sass import Release
from .embedded_sass_pb2 import OutboundMessage, InboundMessage
from .embedded_sass_pb2 import Syntax, OutputStyle

from ..simple import Result

from .sass_function import SassFunction

if TYPE_CHECKING:
    from typing import Optional, Sequence

    from ..dart_sass import Executable

logger = logging.getLogger(__name__)


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


class Compiler():

    executable: Executable
    _async_proc: asyncio.subprocess.Process
    _inbound_queue: asyncio.Queue[InboundMessage]
    _outbound_queue: asyncio.Queue[OutboundMessage]
    _id: int




    def __init__(self):
        self.executable = Release.init().get_executable()
        self._async_proc = None
        self._inbound_queue = asyncio.Queue()
        self._outbound_queue = asyncio.Queue()
        self._id = 1

        self._scss_string: Optional[str] = None
        self._scss_url: Optional[str] = None
        self._syntax: Syntax = Syntax.SCSS

        self._scss_path: Optional[Path] = None
        self._scss_output_style: OutputStyle = OutputStyle.EXPANDED

        self._source_map: bool = False
        self._embed_sources: bool = False
        self._include_paths: list[Path] = []

        self._custom_functions: Sequence[SassFunction] = []

        self._versions: dict[str, str] = {}
        self._css: Optional[str] = None
        self._error: Optional[str] = None



    async def read_packets(self, stdout):
        logger.debug("reading packets...")

        data = b""

        while self._async_proc.returncode is None:
            try:
                data +=await asyncio.wait_for(stdout.read(8), timeout=1.0)
                if not data:
                    break
            except asyncio.TimeoutError:
                break


            length, length_idx = varint.decode_varint(data, 0)
            packet_end = length_idx + length
            # full packet received
            if length <= len(data[length_idx:]):
                
                # second varint is the compilation id
                cid, cidx = varint.decode_varint(data, length_idx)
                msg = OutboundMessage()
                msg.ParseFromString(data[cidx:packet_end])
                await self._outbound_queue.put(msg)

                data = data[packet_end:]
  
    def make_packet(self, message: InboundMessage) -> Packet:
        """Convert from protobuf message to packet structure.

        :param message: Sending message.
        :returns: Packet component.
        """
        cid = 0 if message.WhichOneof("message") == "version_request" else self._id
        if cid:
            self._id += 1
        return Packet(compilation_id=cid, message=message)
    
    async def create_version_request(self) -> None:
        request = InboundMessage()
        request.version_request.id = 0

        await self._inbound_queue.put(request)
        
    
    async def create_compile_request(self) -> None:
        request = InboundMessage()

        if self._scss_string:
            request.compile_request.string.source = dedent(self._scss_string)

            # url of the source string
            if self._scss_url:
                request.compile_request.string.url = self._scss_url
            
            request.compile_request.string.syntax = self._syntax

            # importer options can be added here, we are using default importers for now


        elif self._scss_path:
            request.compile_request.file.path = str(self._scss_path)
        else:
            raise RuntimeError("No SCSS source specified for compilation.")
        
        request.compile_request.style = self._scss_output_style

        if self._source_map or self._embed_sources:
            request.compile_request.source_map = True
        
        if self._embed_sources:
            request.compile_request.source_map_include_sources = True

        # add include paths
        for lp in self._include_paths:
            importer = request.compile_request.importers.add()
            importer.path = str(lp)

        # add global functions
        for func in self._custom_functions:
            request.compile_request.global_functions.append(func.signature)

        await self._inbound_queue.put(request)


    

    async def run(self):
        """Send message to Dart Sass process asynchronously."""

        command = [
            self.executable.dart_vm_path,
            self.executable.sass_snapshot_path,
            "--embedded",
        ]

        self._async_proc = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            text=False,
            bufsize=0,
        )

        inbound = await self._inbound_queue.get() 
        packet = self.make_packet(inbound)
        self._async_proc.stdin.write(packet.to_bytes())  # type: ignore[union-

        # Read the response
        await self.read_packets(self._async_proc.stdout)

        task = asyncio.create_task(self.worker())

        await task

        self._async_proc.stdin.close()
        await self._async_proc.wait()

    async def worker(self):
        while True:
            message = await self._outbound_queue.get()
            if message is None:
                break
            
            if message.WhichOneof('message') == 'error':
                logger.error(f"Sass Error: {message.error.message}")
                break
            if message.WhichOneof('message') == 'log_event':
                logger.info(f"Sass Log: {message.log_event.message}")
            if message.WhichOneof('message') == 'compile_response':

                if message.compile_response.WhichOneof("result") == "failure":
                    self._error = message.compile_response.failure.message
                    logger.error(f"Sass Compilation Failed: {self._error}")
                    break
                logger.debug("Received compile response.")
                self._css = message.compile_response.success.css
                self._source_map = message.compile_response.success.source_map
                break

            if message.WhichOneof('message') == 'version_response':
                logger.debug("Received version response.")
                self._versions["compiler_version"] = message.version_response.compiler_version
                self._versions["protocol_version"] = message.version_response.protocol_version
                self._versions["implementation_version"] = message.version_response.implementation_version
                self._versions["implementation_name"] = message.version_response.implementation_name
                break

            if message.WhichOneof('message') == 'import_request':
                logger.debug("Received import request.")
                # Handle import request if needed
                pass
            if message.WhichOneof('message') == 'file_import_request':
                logger.debug("Received file import request.")
                # Handle file import request if needed
                pass
            if message.WhichOneof('message') == 'function_call_request':
                logger.debug("Received function call request.")
                # Handle function call request if needed
                pass
            if message.WhichOneof('message') == 'canonicalize_request':
                logger.debug("Received canonicalize request.")
                # Handle async function call request if needed
                pass

    def get_version_info(self) -> dict[str, str]:
        """Get version information from Dart Sass process.

        :returns: A dictionary containing version information.
        :rtype: dict[str, str]
        """
        async def _get_version():
            await self.create_version_request()
            await self.run()
        
        asyncio.run(_get_version())

        return self._versions
    
    
    def compile_string(self, 
                       source: str, 
                       syntax: Syntax = Syntax.SCSS, 
                       load_paths: Optional[list[Path]] = None,
                       style: OutputStyle = OutputStyle.EXPANDED,
                       embed_sourcemap: bool = False,
                       embed_sources: bool = False) -> Result[str]:
        """Compile SCSS string to CSS.

        :param source: SCSS source string.
        :param syntax: Syntax of the source string (SCSS or SASS).
        :param embed_sourcemap: Whether to embed source map.
        :param embed_sources: Whether to embed sources in source map.
        :returns: Compiled CSS string.
        :rtype: str
        """
        self._scss_string = source
        self._syntax = syntax
        if load_paths:
            self._include_paths = load_paths
        self._scss_output_style = style
        self._source_map = embed_sourcemap
        self._embed_sources = embed_sources

        async def _compile():
            await self.create_compile_request()
            await self.run()
        
        asyncio.run(_compile())

        # Return error result if compilation failed
        if self._error:
            return Result(False, error=self._error)
        
        # Add trailing newline to match expected output format
        css_output = self._css + '\n' if self._css and not self._css.endswith('\n') else self._css
        return Result(True, output=css_output)


