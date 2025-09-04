"""Utility helpers for PyOrion."""

import dataclasses
import socket
from pathlib import Path
from typing import Any

from pydantic import BaseModel


def find_folder(folder_name: str) -> Path | None:
    """Search for a folder starting from the current working directory."""
    start_path = Path.cwd()
    for path in start_path.rglob(folder_name):
        if path.is_dir():
            return path
    return None


def load_html(path: Path | str | None) -> str:
    """Load HTML content from a file or return a fallback message."""
    if path is None:
        return _fallback_html()

    html_src = Path.cwd() / path
    if not html_src.exists():
        return _fallback_html()

    return html_src.read_text(encoding="utf-8")


def _fallback_html() -> str:
    """Return a default HTML snippet as fallback content."""
    return r""" ... """


def find_free_ports_and_create_addrs() -> str:
    """Find a free TCP port and return a localhost address."""

    def find_free_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("", 0))
            return sock.getsockname()[1]

    port = find_free_port()
    return f"127.0.0.1:{port}"


def split_address(address: str) -> tuple[str, int]:
    """Split an address of the form ``host:port`` into host and port."""
    if ":" not in address:
        msg = f"Invalid address format: {address!r}. Expected: 'host:port'."
        raise ValueError(msg)

    host, port_str = address.rsplit(":", 1)

    if not host:
        raise ValueError("Host part must not be empty.")
    if not port_str:
        raise ValueError("Port part must not be empty.")

    try:
        port = int(port_str)
        if not (0 <= port <= 65535):
            raise ValueError(f"Port must be between 0 and 65535: {port}")
    except ValueError as exc:
        raise ValueError(f"Invalid port: {port_str!r}. Must be an integer.") from exc

    return host, port


def make_json_safe(obj: Any) -> Any:
    """Convert arbitrary Python objects into JSON-serializable structures."""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [make_json_safe(v) for v in obj]
    return str(obj)


def normalize_args(args: Any | None) -> list[Any]:
    """Normalize arguments to a JSON-safe list."""
    if args is None:
        return []
    if isinstance(args, list):
        return [make_json_safe(a) for a in args]
    return [make_json_safe(args)]
