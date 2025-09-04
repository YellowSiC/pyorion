use anyhow::Result;
use pyorion_macros::api;

use crate::api_manager::ApiManager;

pub fn register_api_instances(api_manager: &mut ApiManager) {
    api_manager.register_api("webview.isDevtoolsOpen", is_devtools_open);
    api_manager.register_api("webview.openDevtools", open_devtools);
    api_manager.register_api("webview.closeDevtools", close_devtools);
}

#[api]
fn is_devtools_open() -> Result<bool> {
    let webview = app.app_context()?.get_webview()?;
    Ok(webview.is_devtools_open())
}

#[api]
fn open_devtools() -> Result<()> {
    let webview = app.app_context()?.get_webview()?;
    webview.open_devtools();
    Ok(())
}

#[api]
fn close_devtools() -> Result<()> {
    let webview = app.app_context()?.get_webview()?;
    webview.close_devtools();
    Ok(())
}
