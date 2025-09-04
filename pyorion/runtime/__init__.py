"""Runtime package for PyOrion.

This package provides the main entry point for launching the
native runtime environment that manages event loops, process
spawning, and communication with the Rust backend.

Exports
-------
* :func:`launch` — alias for :func:`run_native_runtime`
  to start the runtime.
"""

from .runtime import run_native_runtime as launch


__all__ = [
    "launch",
]
