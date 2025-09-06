import asyncio
import base64
from io import BytesIO

import matplotlib.pyplot as plt
from nicegui import app, ui
from PIL import Image

from pyorion import launch
from pyorion.api.clipboard import ClipboardAPI
from pyorion.api.controlcenter import ControlCenterAPI
from pyorion.api.dialog import DialogAPI
from pyorion.api.dirs import DirsAPI
from pyorion.api.webview import WebView
from pyorion.api.window import Window
from pyorion.setup import types


clipboard = ClipboardAPI()
control = ControlCenterAPI()
dialogs = DialogAPI()
dirs = DirsAPI()
webview = WebView()
window = Window()


# ---------- Clipboard ----------
@ui.page("/clipboard")
def page_clipboard() -> None:
    with ui.column().classes("p-6"):
        ui.label("📋 Clipboard API").classes("text-xl font-bold")
        text_input = ui.input("Text eingeben").classes("w-full")
        ui.button(
            "Set Text",
            on_click=lambda: asyncio.create_task(clipboard.set_text(text_input.value)),
        )
        ui.button(
            "Get Text", on_click=lambda: asyncio.create_task(show_clipboard_text())
        )
        ui.button("Clear", on_click=lambda: asyncio.create_task(clipboard.clear()))


async def show_clipboard_text() -> None:
    text = await clipboard.get_text()
    ui.notify(f"Clipboard: {text}")


# ---------- ControlCenter ----------
@ui.page("/controlcenter")
def page_controlcenter() -> None:
    with ui.column().classes("p-6"):
        ui.label("🔔 ControlCenter API").classes("text-xl font-bold")
        notif_text = ui.input("Notification Text").classes("w-full")
        ui.button(
            "Send Notification",
            on_click=lambda: asyncio.create_task(
                control.notification(
                    summary=notif_text.value, body="Hello from NiceGUI"
                )
            ),
        )


# ---------- Dialog ----------
@ui.page("/dialog")
def page_dialog() -> None:
    with ui.column().classes("p-6"):
        ui.label("💬 Dialog API").classes("text-xl font-bold")
        ui.button(
            "Show Message",
            on_click=lambda: asyncio.create_task(
                dialogs.show_message("Info", "Das ist eine Testnachricht")
            ),
        )
        ui.button("Pick File", on_click=lambda: asyncio.create_task(pick_file()))


async def pick_file() -> None:
    result = await dialogs.pick_file()
    ui.notify(f"Picked: {result}")


# ---------- Dirs ----------
@ui.page("/dirs")
def page_dirs() -> None:
    with ui.column().classes("p-6"):
        ui.label("📂 Dirs API").classes("text-xl font-bold")
        ui.button("Get Home Dir", on_click=lambda: asyncio.create_task(show_home()))


async def show_home() -> None:
    home = await dirs.home_dir()
    ui.notify(f"Home Dir: {home}")


# ---------- WebView ----------
@ui.page("/webview")
def page_webview() -> None:
    with ui.column().classes("p-6"):
        ui.label("🌐 WebView API").classes("text-xl font-bold")
        ui.button(
            "Open DevTools",
            on_click=lambda: asyncio.create_task(webview.open_devtools()),
        )
        ui.button(
            "Close DevTools",
            on_click=lambda: asyncio.create_task(webview.close_devtools()),
        )


# ---------- Window ----------
@ui.page("/window")
def page_window() -> None:
    with ui.column().classes("p-6"):
        ui.label("🪟 Window API").classes("text-xl font-bold")
        title_input = ui.input("Fenstertitel").classes("w-full")
        ui.button(
            "Set Title",
            on_click=lambda: asyncio.create_task(window.set_title(title_input.value)),
        )
        ui.button("Get Title", on_click=lambda: asyncio.create_task(show_title()))


async def show_title() -> None:
    title = await window.get_title()
    ui.notify(f"Window Title: {title}")


# ---------- Sidebar Navigation ----------
@ui.page("/")
def main_page() -> None:
    with ui.row().classes("p-6"):
        ui.label("PyOrion Control Center").classes("text-2xl font-bold")

    with ui.column().classes("p-6"):
        ui.link("📋 Clipboard", "/clipboard")
        ui.link("🔔 ControlCenter", "/controlcenter")
        ui.link("💬 Dialog", "/dialog")
        ui.link("📂 Dirs", "/dirs")
        ui.link("🌐 WebView", "/webview")
        ui.link("🪟 Window", "/window")


ui.run(title="PyOrion API Control")


async def run_runtime() -> None:
    app_cfg = types.WindowOptions(
        title="Scientific Dashboard",
        inner_size=types.Size(width=1200, height=800, unit=types.UnitType.logical),
        resizable=True,
        transparent=True,
        decorations=True,
        webview=types.WebViewOptions(
            label="root",
            render_protocol="http://localhost:8080",
            visible=True,
            devtools=True,
        ),
    )
    await launch(app_cfg)


async def apply_effect(effect: types.WindowEffect, name: str) -> None:
    ok = await window.set_window_effect(
        effects=[effect],
        state=types.WindowEffectState.Active,
        color=types.Color.from_hex("#3366FFAA"),  # halbtransparentes Blau
    )
    if ok:
        await dialogs.show_message("WindowEffect", f"{name} aktiviert ✅", "info")
    else:
        await dialogs.show_message(
            "WindowEffect", f"{name} fehlgeschlagen ❌", "warning"
        )


async def handle_set_text() -> None:
    await clipboard.set_text("Hallo von PyOrion Clipboard!")
    await dialogs.show_message("Clipboard", "Text gesetzt ✅", "info")


async def handle_get_text() -> None:
    text = await clipboard.get_text()
    await dialogs.show_message("Clipboard Inhalt", text or "Leer", "info")


async def handle_clear() -> None:
    await clipboard.clear()
    await dialogs.show_message("Clipboard", "Clipboard geleert 🗑️", "info")


async def handle_set_image() -> None:
    img = Image.new("RGBA", (200, 150), (200, 50, 50, 255))
    raw_bytes = img.tobytes()
    await clipboard.set_image(200, 150, raw_bytes)
    await dialogs.show_message("Clipboard", "Bild ins Clipboard geschrieben ✅", "info")


async def handle_get_image() -> None:
    width, height, raw_bytes = await clipboard.get_image()
    if not raw_bytes:
        await dialogs.show_message("Clipboard", "Kein Bild im Clipboard ❌", "warning")
        return

    img = Image.frombytes("RGBA", (width, height), raw_bytes)
    buf = BytesIO()
    img.save(buf, format="PNG")
    data_url = f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"

    ui.image(data_url).style(
        "max-width: 220px; border-radius: 16px; "
        "box-shadow: 0 6px 12px rgba(0,0,0,0.25);"
    )
    await dialogs.show_message(
        "Clipboard", f"Bild geladen ({width}x{height}) ✅", "info"
    )


with ui.header().classes(
    "bg-gradient-to-r from-blue-700 to-blue-500 text-white shadow-lg p-4 flex justify-between items-center"
):
    ui.label("🔬 Scientific Dashboard").classes("text-2xl font-bold")
    ui.label("Powered by PyOrion + NiceGUI").classes("text-sm italic text-gray-200")


with ui.row().classes("grid grid-cols-3 gap-8 p-6 w-full"):
    with ui.card().classes(
        "flex flex-col items-center justify-center rounded-2xl shadow-xl p-6"
    ):
        ui.label("📋 Clipboard: Text").classes("text-lg font-semibold mb-2")
        ui.button("Set Text", on_click=lambda _: handle_set_text()).classes("w-full")
        ui.button("Get Text", on_click=lambda _: handle_get_text()).classes("w-full")
        ui.button("Clear Clipboard", on_click=lambda _: handle_clear()).classes(
            "w-full"
        )
    with ui.card().classes(
        "flex flex-col items-center justify-center rounded-2xl shadow-xl p-6"
    ):
        ui.label("🖼️ Clipboard: Bilder").classes("text-lg font-semibold mb-2")
        ui.button("Set Test Image", on_click=lambda _: handle_set_image()).classes(
            "w-full"
        )
        ui.button("Get Image", on_click=lambda _: handle_get_image()).classes("w-full")
with ui.row().classes("grid grid-cols-3 gap-6 p-6 w-full"):
    with ui.card().classes("p-4 rounded-xl shadow-lg"):
        ui.label("Basic").classes("font-semibold mb-2")
        ui.button(
            "Blur", on_click=lambda _: apply_effect(types.WindowEffect.Blur, "Blur")
        )
        ui.button(
            "Acrylic",
            on_click=lambda _: apply_effect(types.WindowEffect.Acrylic, "Acrylic"),
        )

    with ui.card().classes("p-4 rounded-xl shadow-lg"):
        ui.label("Mica (Win11)").classes("font-semibold mb-2")
        ui.button(
            "Mica", on_click=lambda _: apply_effect(types.WindowEffect.Mica, "Mica")
        )
        ui.button(
            "Mica Dark",
            on_click=lambda _: apply_effect(types.WindowEffect.MicaDark, "MicaDark"),
        )
        ui.button(
            "Mica Light",
            on_click=lambda _: apply_effect(types.WindowEffect.MicaLight, "MicaLight"),
        )

    with ui.card().classes("p-4 rounded-xl shadow-lg"):
        ui.label("Tabbed (Win11)").classes("font-semibold mb-2")
        ui.button(
            "Tabbed",
            on_click=lambda _: apply_effect(types.WindowEffect.Tabbed, "Tabbed"),
        )
        ui.button(
            "Tabbed Dark",
            on_click=lambda _: apply_effect(
                types.WindowEffect.TabbedDark, "TabbedDark"
            ),
        )
        ui.button(
            "Tabbed Light",
            on_click=lambda _: apply_effect(
                types.WindowEffect.TabbedLight, "TabbedLight"
            ),
        )

with ui.card().classes("m-6 p-6 shadow-xl rounded-2xl"):
    ui.label("📊 Plot Demo").classes("text-lg font-semibold mb-4")
    with ui.pyplot(figsize=(4, 3)) as fig:
        plt.plot([0, 1, 2, 3], [0, 1, 4, 9], marker="o")
        plt.title("Quadratische Funktion")
        plt.grid(True)


# Launch the WebView window on startup
app.on_startup(run_runtime)

ui.run(show=False)
