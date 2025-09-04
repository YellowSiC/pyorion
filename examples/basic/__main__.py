"""Entry point for the basic PyOrion example.

This script launches the PyOrion runtime with predefined
window options and registers basic commands.
"""

import asyncio
import sys

from pyorion import launch

from ..basic import commands
from .config import window_options_config


if __name__ == "__main__":
    try:
        asyncio.run(
            launch(init_options=window_options_config, host="127.0.0.1", port=9000)
        )
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
