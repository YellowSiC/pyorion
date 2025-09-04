use base64::Engine;
use base64::engine::general_purpose::STANDARD;
use serde::{Deserialize, Serialize};
use tao::dpi::{
    LogicalPosition, LogicalSize, PhysicalPosition, PhysicalSize, Position as DpiPosition,
    Size as DpiSize,
};
use tao::window::{
    CursorIcon as TaoCursorIcon, Icon as TaoWindowIcon, ProgressBarState as TaoProgressBarState,
    ProgressState as TaoProgressState, Theme as TaoTheme,
    UserAttentionType as TaoUserAttentionType, WindowSizeConstraints as TaoWindowSizeConstraints,
};
use wry::Rect;

#[derive(Deserialize, Clone, Debug, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum UnitType {
    Logical,
    Physical,
}

#[derive(Deserialize, Clone, Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Position {
    pub x: Option<i32>,
    pub y: Option<i32>,
    pub unit: UnitType,
}

#[derive(Deserialize, Clone, Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Size {
    pub width: Option<i32>,
    pub height: Option<i32>,
    pub unit: UnitType,
}

#[derive(Deserialize, Clone, Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct WebViewBounds {
    pub position: Position,
    pub size: Size,
}

impl From<Position> for LogicalPosition<f64> {
    fn from(value: Position) -> Self {
        LogicalPosition {
            x: value.x.unwrap_or(0) as f64,
            y: value.y.unwrap_or(0) as f64,
        }
    }
}

impl From<Position> for PhysicalPosition<i32> {
    fn from(value: Position) -> Self {
        PhysicalPosition {
            x: value.x.unwrap_or(0),
            y: value.y.unwrap_or(0),
        }
    }
}

impl From<Size> for LogicalSize<f64> {
    fn from(value: Size) -> Self {
        LogicalSize {
            width: value.width.unwrap_or(0) as f64,
            height: value.height.unwrap_or(0) as f64,
        }
    }
}

impl From<Size> for PhysicalSize<u32> {
    fn from(value: Size) -> Self {
        PhysicalSize {
            width: value.width.unwrap_or(0).max(0) as u32,
            height: value.height.unwrap_or(0).max(0) as u32,
        }
    }
}

impl From<Position> for DpiPosition {
    fn from(value: Position) -> Self {
        match value.unit {
            UnitType::Logical => DpiPosition::Logical(LogicalPosition {
                x: value.x.unwrap_or(0) as f64,
                y: value.y.unwrap_or(0) as f64,
            }),
            UnitType::Physical => DpiPosition::Physical(PhysicalPosition {
                x: value.x.unwrap_or(0),
                y: value.y.unwrap_or(0),
            }),
        }
    }
}

impl From<Size> for DpiSize {
    fn from(value: Size) -> Self {
        match value.unit {
            UnitType::Logical => DpiSize::Logical(value.into()),
            UnitType::Physical => DpiSize::Physical(value.into()),
        }
    }
}

impl From<WebViewBounds> for Rect {
    fn from(value: WebViewBounds) -> Self {
        Rect {
            position: value.position.into(),
            size: value.size.into(),
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub enum CursorIcon {
    Default,
    Crosshair,
    Hand,
    Arrow,
    Move,
    Text,
    Wait,
    Help,
    Progress,
    NotAllowed,
    ContextMenu,
    Cell,
    VerticalText,
    Alias,
    Copy,
    NoDrop,
    Grab,
    Grabbing,
    AllScroll,
    ZoomIn,
    ZoomOut,
    EResize,
    NResize,
    NeResize,
    NwResize,
    SResize,
    SeResize,
    SwResize,
    WResize,
    EwResize,
    NsResize,
    NeswResize,
    NwseResize,
    ColResize,
    RowResize,
}

impl From<CursorIcon> for TaoCursorIcon {
    fn from(icon: CursorIcon) -> Self {
        match icon {
            CursorIcon::Default => TaoCursorIcon::Default,
            CursorIcon::Crosshair => TaoCursorIcon::Crosshair,
            CursorIcon::Hand => TaoCursorIcon::Hand,
            CursorIcon::Arrow => TaoCursorIcon::Arrow,
            CursorIcon::Move => TaoCursorIcon::Move,
            CursorIcon::Text => TaoCursorIcon::Text,
            CursorIcon::Wait => TaoCursorIcon::Wait,
            CursorIcon::Help => TaoCursorIcon::Help,
            CursorIcon::Progress => TaoCursorIcon::Progress,
            CursorIcon::NotAllowed => TaoCursorIcon::NotAllowed,
            CursorIcon::ContextMenu => TaoCursorIcon::ContextMenu,
            CursorIcon::Cell => TaoCursorIcon::Cell,
            CursorIcon::VerticalText => TaoCursorIcon::VerticalText,
            CursorIcon::Alias => TaoCursorIcon::Alias,
            CursorIcon::Copy => TaoCursorIcon::Copy,
            CursorIcon::NoDrop => TaoCursorIcon::NoDrop,
            CursorIcon::Grab => TaoCursorIcon::Grab,
            CursorIcon::Grabbing => TaoCursorIcon::Grabbing,
            CursorIcon::AllScroll => TaoCursorIcon::AllScroll,
            CursorIcon::ZoomIn => TaoCursorIcon::ZoomIn,
            CursorIcon::ZoomOut => TaoCursorIcon::ZoomOut,
            CursorIcon::EResize => TaoCursorIcon::EResize,
            CursorIcon::NResize => TaoCursorIcon::NResize,
            CursorIcon::NeResize => TaoCursorIcon::NeResize,
            CursorIcon::NwResize => TaoCursorIcon::NwResize,
            CursorIcon::SResize => TaoCursorIcon::SResize,
            CursorIcon::SeResize => TaoCursorIcon::SeResize,
            CursorIcon::SwResize => TaoCursorIcon::SwResize,
            CursorIcon::WResize => TaoCursorIcon::WResize,
            CursorIcon::EwResize => TaoCursorIcon::EwResize,
            CursorIcon::NsResize => TaoCursorIcon::NsResize,
            CursorIcon::NeswResize => TaoCursorIcon::NeswResize,
            CursorIcon::NwseResize => TaoCursorIcon::NwseResize,
            CursorIcon::ColResize => TaoCursorIcon::ColResize,
            CursorIcon::RowResize => TaoCursorIcon::RowResize,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub enum ProgressState {
    None,
    Normal,
    Indeterminate,
    Paused,
    Error,
}

impl From<ProgressState> for TaoProgressState {
    fn from(state: ProgressState) -> Self {
        match state {
            ProgressState::None => TaoProgressState::None,
            ProgressState::Normal => TaoProgressState::Normal,
            ProgressState::Indeterminate => TaoProgressState::Indeterminate,
            ProgressState::Paused => TaoProgressState::Paused,
            ProgressState::Error => TaoProgressState::Error,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ProgressBarState {
    pub progress: Option<u64>,
    pub status: Option<ProgressState>,
    pub desktop_filename: Option<String>,
}

impl From<ProgressBarState> for TaoProgressBarState {
    fn from(state: ProgressBarState) -> Self {
        TaoProgressBarState {
            progress: state.progress,
            state: state.status.map(|s| s.into()),
            desktop_filename: state.desktop_filename,
        }
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
pub enum Theme {
    Light,
    Dark,
}

impl From<Theme> for TaoTheme {
    fn from(theme: Theme) -> Self {
        match theme {
            Theme::Light => TaoTheme::Light,
            Theme::Dark => TaoTheme::Dark,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub enum UserAttentionType {
    Critical,
    Informational,
}

impl From<UserAttentionType> for TaoUserAttentionType {
    fn from(att: UserAttentionType) -> Self {
        match att {
            UserAttentionType::Critical => TaoUserAttentionType::Critical,
            UserAttentionType::Informational => TaoUserAttentionType::Informational,
        }
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct ByteIcon {
    pub rgba: String, // Base64-encoded
    pub width: u32,
    pub height: u32,
}

impl From<ByteIcon> for TaoWindowIcon {
    fn from(icon: ByteIcon) -> Self {
        let bytes = STANDARD.decode(&icon.rgba).unwrap_or_default();
        TaoWindowIcon::from_rgba(bytes, icon.width, icon.height).unwrap()
    }
}
#[allow(dead_code)]
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct Icon {
    pub path: String,
}

impl Icon {
    #[allow(dead_code)]
    pub fn to_icon(&self) -> anyhow::Result<TaoWindowIcon> {
        let bytes = std::fs::read(&self.path)?;
        let image = image::load_from_memory(&bytes)?.to_rgba8();
        let (width, height) = image.dimensions();
        Ok(TaoWindowIcon::from_rgba(image.into_raw(), width, height)?)
    }
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Dimensions {
    /// The width of the size.
    pub width: u32,
    /// The height of the size.
    pub height: u32,
}

/// Serde-kompatibles Constraints-Objekt
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct WindowSizeConstraints {
    pub min_width: Option<f64>,
    pub min_height: Option<f64>,
    pub max_width: Option<f64>,
    pub max_height: Option<f64>,
    pub unit: UnitType,
}

impl From<WindowSizeConstraints> for TaoWindowSizeConstraints {
    fn from(c: WindowSizeConstraints) -> Self {
        let (min_width, min_height, max_width, max_height) = match c.unit {
            UnitType::Logical => (
                c.min_width
                    .map(|w| tao::dpi::PixelUnit::Logical(tao::dpi::LogicalUnit::new(w))),
                c.min_height
                    .map(|h| tao::dpi::PixelUnit::Logical(tao::dpi::LogicalUnit::new(h))),
                c.max_width
                    .map(|w| tao::dpi::PixelUnit::Logical(tao::dpi::LogicalUnit::new(w))),
                c.max_height
                    .map(|h| tao::dpi::PixelUnit::Logical(tao::dpi::LogicalUnit::new(h))),
            ),
            UnitType::Physical => (
                c.min_width.map(|w| {
                    tao::dpi::PixelUnit::Physical(tao::dpi::PhysicalUnit::new(
                        (w as u32).try_into().unwrap(),
                    ))
                }),
                c.min_height.map(|h| {
                    tao::dpi::PixelUnit::Physical(tao::dpi::PhysicalUnit::new(
                        (h as u32).try_into().unwrap(),
                    ))
                }),
                c.max_width.map(|w| {
                    tao::dpi::PixelUnit::Physical(tao::dpi::PhysicalUnit::new(
                        (w as u32).try_into().unwrap(),
                    ))
                }),
                c.max_height.map(|h| {
                    tao::dpi::PixelUnit::Physical(tao::dpi::PhysicalUnit::new(
                        (h as u32).try_into().unwrap(),
                    ))
                }),
            ),
        };

        TaoWindowSizeConstraints {
            min_width,
            min_height,
            max_width,
            max_height,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct MonitorVideoMode {
    /// The size of the video mode.
    pub size: Dimensions,
    /// The bit depth of the video mode.
    pub bit_depth: u16,
    /// The refresh rate of the video mode.
    pub refresh_rate: u16,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Monitor {
    /// The name of the monitor.
    pub name: Option<String>,
    /// The scale factor of the monitor.
    pub scale_factor: f64,
    /// The size of the monitor.
    pub size: Dimensions,
    /// The position of the monitor.
    pub position: MonitorPosition,
    /// The video modes of the monitor.
    pub video_modes: Vec<MonitorVideoMode>,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct MonitorPosition {
    /// The x position.
    pub x: i32,
    /// The y position.
    pub y: i32,
}

#[allow(dead_code)]
#[derive(Deserialize, Clone, Debug, Default)]
#[serde(rename_all = "camelCase")]
pub struct WindowOptions {
    pub always_on_bottom: Option<bool>,
    pub always_on_top: Option<bool>,
    pub background_color: Option<(u8, u8, u8, u8)>, // RGBA
    pub closable: Option<bool>,
    pub content_protection: Option<bool>,
    pub decorations: Option<bool>,
    pub focusable: Option<bool>,
    pub focused: Option<bool>,
    pub fullscreen: Option<bool>,
    pub inner_size: Option<Size>,
    pub max_inner_size: Option<Size>,
    pub maximizable: Option<bool>,
    pub maximized: Option<bool>,
    pub min_inner_size: Option<Size>,
    pub minimizable: Option<bool>,
    pub position: Option<Position>,
    pub resizable: Option<bool>,
    pub theme: Option<Theme>,
    pub title: Option<String>,
    pub transparent: Option<bool>,
    pub visible: Option<bool>,
    pub visible_on_all_workspaces: Option<bool>,
    pub window_icon: Option<Icon>,
    pub webview: WebViewOptions,
}
#[allow(dead_code)]
#[derive(Deserialize, Clone, Debug, Default)]
#[serde(rename_all = "camelCase")]
pub struct WebViewOptions {
    pub label: Option<String>,
    pub render_protocol: Option<String>,
    pub transparent: Option<bool>,
    pub visible: Option<bool>,
    pub devtools: Option<bool>,
    pub incognito: Option<bool>,
    pub user_agent: Option<String>,
    pub initialization_script: Option<String>,
    pub accept_first_mouse: Option<bool>,
    pub autoplay: Option<bool>,
    pub focused: Option<bool>,
    pub clipboard: Option<bool>,
    pub hotkeys_zoom: Option<bool>,
    pub background_color: Option<(u8, u8, u8, u8)>,
    pub bounds: Option<WebViewBounds>, // x, y, w, h
    pub headers: Option<std::collections::HashMap<String, String>>,
    pub proxy_config: Option<String>,
    pub zoom_hotkeys: Option<bool>,
    pub background_throttling: Option<bool>,
    pub back_forward_navigation_gestures: Option<bool>,
}
