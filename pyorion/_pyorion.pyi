import multiprocessing
from typing import Any

__version__: str
"""The package version as defined in `Cargo.toml`, modified to match python's versioning semantics."""

def create_webframe(
    config: str,
    host: str,
    port: int,
    uds_name: str,
    close_event: multiprocessing.Event,  # type: ignore
) -> Any: ...
async def send_event_over_platform(
    name: str,
    message: str,
) -> Any: ...
