from typing import Any

from PIL import Image

from pyorion import command
from pyorion.api.clipboard import ClipboardAPI
from pyorion.api.controlcenter import ControlCenterAPI
from pyorion.api.dialog import DialogAPI
from pyorion.api.dirs import DirsAPI
from pyorion.api.webview import WebView
from pyorion.api.window import Window
from pyorion.setup.types import ClipboardImage


clipboard = ClipboardAPI()
control = ControlCenterAPI()
dialogs = DialogAPI()
dirs = DirsAPI()
webview = WebView()
window = Window()


# -------- Clipboard --------
@command
async def set_text(text: str) -> bool:
    return await clipboard.set_text(text)


@command
async def get_text() -> str:
    return await clipboard.get_text()


@command
async def clear() -> bool:
    return await clipboard.clear()


@command
async def set_image() -> bool:
    img = Image.new("RGBA", (100, 100), (200, 50, 50, 255))
    raw_bytes = img.tobytes()
    return await clipboard.set_image(100, 100, raw_bytes)


@command
async def get_image() -> ClipboardImage:
    data = await clipboard.get_image()
    return data


# -------- ControlCenter --------
@command
async def notification(summary: str, body: str) -> bool:
    return await control.notification(summary=summary, body=body)


# -------- Dialog --------
@command
async def show_message(title: str, message: str) -> bool:
    return await dialogs.show_message(title, message)


@command
async def pick_file() -> dict[str, Any]:
    return await dialogs.pick_file()


# -------- Dirs --------
@command
async def home_dir() -> str:
    return await dirs.home_dir()


# -------- WebView --------
@command
async def open_devtools() -> None:
    return await webview.open_devtools()


@command
async def close_devtools() -> None:
    return await webview.close_devtools()


# -------- Window --------
@command
async def set_title(title: str) -> bool:
    return await window.set_title(title)


@command
async def get_title() -> str:
    return await window.get_title()


@command
async def set_fullscreen(state: bool) -> bool:
    return await window.set_fullscreen(state)
