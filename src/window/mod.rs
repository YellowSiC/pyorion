use pyorion_options::window::WindowOptions;
use tao::window::{Window, WindowId};
use wry::WebView;

use crate::{utils::FrameWindowTarget, window::builder::FrameBuilder};

pub(crate) mod builder;

pub fn create_frame(
    target: &FrameWindowTarget,
    options: &WindowOptions,
    init_add: String,
) -> anyhow::Result<(WindowId, Window, WebView)> {
    let window = FrameBuilder::build_window(target, options)?;
    let id = window.id();
    let webview = FrameBuilder::build_webview(&window, &options.webview, init_add)?;
    Ok((id, window, webview))
}
