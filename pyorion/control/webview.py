"""WebView control API for PyOrion."""

from ..runtime.runtime_handle import event_register


class WebView:
    """High-level wrapper for controlling a WebView instance."""

    def __init__(self) -> None:
        """Initialize a WebView handle."""

    async def is_devtools_open(self) -> bool:  # N802 gefixt
        """Check if the DevTools window is currently open."""
        return await event_register("webview.isDevtoolsOpen", None, result_type=bool)

    async def open_devtools(self) -> bool:
        """Open the DevTools window."""
        return await event_register("webview.openDevtools", None, result_type=bool)

    async def close_devtools(self) -> bool:
        """Close the DevTools window."""
        return await event_register("webview.closeDevtools", None, result_type=bool)
