use crate::api_manager::ApiManager;
mod webview;
mod window;

pub fn register_api_instances(api_manager: &mut ApiManager) {
    window::register_api_instances(api_manager);
    webview::register_api_instances(api_manager);
}
