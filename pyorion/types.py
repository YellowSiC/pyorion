"""Datamodel-Typen und Enums für PyOrion."""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_serializer
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """Basisklasse für alle Schemas mit einheitlicher Pydantic-Konfiguration."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class RGBA(BaseSchema):
    """RGBA-Farbmodell, serialisierbar als Tupel (r, g, b, a)."""

    r: int
    g: int
    b: int
    a: int

    def as_tuple(self) -> tuple[int, int, int, int]:
        """Konvertiere RGBA in ein Tupel im Format (r, g, b, a)."""
        return (self.r, self.g, self.b, self.a)

    @model_serializer
    def serialize_as_tuple(self) -> tuple[int, int, int, int]:
        """Serialisiere RGBA als Tupel für Serde-Kompatibilität mit Rust."""
        return self.as_tuple()


class UnitType(str, Enum):
    """Darstellung von Längen-/Größeneinheiten (logisch oder physisch)."""

    logical = "logical"
    physical = "physical"


class Position(BaseSchema):
    """Fenster- oder WebView-Position mit optionalen Koordinaten und Einheit."""

    x: Optional[int] = None
    y: Optional[int] = None
    unit: UnitType


class Size(BaseSchema):
    """Fenster- oder WebView-Größe mit optionalen Dimensionen und Einheit."""

    width: Optional[int] = None
    height: Optional[int] = None
    unit: UnitType


class WebViewBounds(BaseSchema):
    """Kombination aus Position und Größe eines WebViews."""

    position: Position
    size: Size


class CursorIcon(str, Enum):
    """Unterstützte Mauszeiger-Icons für Fenster/WebViews."""

    default = "default"
    crosshair = "crosshair"
    hand = "hand"
    arrow = "arrow"
    move = "move"
    text = "text"
    wait = "wait"
    help = "help"
    progress = "progress"
    not_allowed = "not_allowed"
    context_menu = "context_menu"
    cell = "cell"
    vertical_text = "vertical_text"
    alias = "alias"
    copy = "copy"
    no_drop = "no_drop"
    grab = "grab"
    grabbing = "grabbing"
    all_scroll = "all_scroll"
    zoom_in = "zoom_in"
    zoom_out = "zoom_out"
    e_resize = "e_resize"
    n_resize = "n_resize"
    ne_resize = "ne_resize"
    nw_resize = "nw_resize"
    s_resize = "s_resize"
    se_resize = "se_resize"
    sw_resize = "sw_resize"
    w_resize = "w_resize"
    ew_resize = "ew_resize"
    ns_resize = "ns_resize"
    nesw_resize = "nesw_resize"
    nwse_resize = "nwse_resize"
    col_resize = "col_resize"
    row_resize = "row_resize"


class ProgressState(str, Enum):
    """Zustände einer Fortschrittsanzeige."""

    none = "none"
    normal = "normal"
    indeterminate = "indeterminate"
    paused = "paused"
    error = "error"


class ProgressBarState(BaseSchema):
    """Status einer Fortschrittsanzeige, inkl. Fortschritt und Zustand."""

    progress: Optional[int] = None
    status: Optional[ProgressState] = None
    desktop_filename: Optional[str] = None


class Theme(str, Enum):
    """Farbthema für Fensterdarstellung."""

    light = "light"
    dark = "dark"


class UserAttentionType(str, Enum):
    """Art der Benutzeraufmerksamkeit (kritisch oder informativ)."""

    critical = "critical"
    informational = "informational"


class ByteIcon(BaseSchema):
    """Fenstersymbol als RGBA-Byte-Array (Base64-kodiert)."""

    rgba: str  # base64 encoded
    width: int
    height: int


class Icon(BaseSchema):
    """Fenstersymbol als Dateipfad."""

    path: str


class WindowSizeConstraints(BaseSchema):
    """Minimale und maximale Fenstergrößen mit Einheit."""

    min_width: Optional[float] = None
    min_height: Optional[float] = None
    max_width: Optional[float] = None
    max_height: Optional[float] = None
    unit: UnitType


class Dimensions(BaseSchema):
    """Breite und Höhe als Integer-Dimensionen."""

    width: int
    height: int


class MonitorPosition(BaseSchema):
    """Position eines Monitors auf dem Desktop (x,y)."""

    x: int
    y: int


class MonitorVideoMode(BaseSchema):
    """Video-Modus eines Monitors mit Auflösung, Farbtiefe und Refresh-Rate."""

    size: Dimensions
    bit_depth: int
    refresh_rate: int


class Monitor(BaseSchema):
    """Darstellung eines Monitors mit Name, Skalierung und Video-Modi."""

    name: Optional[str] = None
    scale_factor: float
    size: Dimensions
    position: MonitorPosition
    video_modes: list[MonitorVideoMode]


class WebViewOptions(BaseSchema):
    """Optionen zur Konfiguration eines WebViews."""

    label: Optional[str] = None
    render_protocol: Optional[Path | str] = None
    transparent: Optional[bool] = None
    visible: Optional[bool] = None
    devtools: Optional[bool] = None
    incognito: Optional[bool] = None
    initialization_script: Optional[str] = None
    accept_first_mouse: Optional[bool] = None
    autoplay: Optional[bool] = None
    focused: Optional[bool] = None
    clipboard: Optional[bool] = None
    hotkeys_zoom: Optional[bool] = None
    background_color: Optional[RGBA] = None
    bounds: Optional[WebViewBounds] = None
    headers: Optional[dict[str, str]] = None
    proxy_config: Optional[str] = None
    zoom_hotkeys: Optional[bool] = None
    background_throttling: Optional[bool] = None
    back_forward_navigation_gestures: Optional[bool] = None


class WindowOptions(BaseSchema):
    """Optionen zur Konfiguration eines Fensters."""

    always_on_bottom: Optional[bool] = None
    always_on_top: Optional[bool] = None
    background_color: Optional[RGBA] = None
    closable: Optional[bool] = None
    content_protection: Optional[bool] = None
    decorations: Optional[bool] = None
    focusable: Optional[bool] = None
    focused: Optional[bool] = None
    fullscreen: Optional[bool] = None
    inner_size: Optional[Size] = None
    max_inner_size: Optional[Size] = None
    maximizable: Optional[bool] = None
    maximized: Optional[bool] = None
    min_inner_size: Optional[Size] = None
    minimizable: Optional[bool] = None
    position: Optional[Position] = None
    resizable: Optional[bool] = None
    theme: Optional[Theme] = None
    title: Optional[str] = None
    transparent: Optional[bool] = None
    visible: Optional[bool] = None
    visible_on_all_workspaces: Optional[bool] = None
    window_icon: Optional[Icon] = None
    webview: Optional[WebViewOptions] = None
