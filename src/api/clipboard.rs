// Copyright 2025-2030 Ari Bermeki @ YellowSiC within The Commons Conservancy
// SPDX-License-Identifier: Apache-2.0
// SPDX-License-Identifier: MIT
use crate::api_manager::ApiManager;
use arboard::{Clipboard, ImageData};
use once_cell::sync::Lazy;
use pyorion_macros::api;
use serde::Serialize;
use std::sync::Mutex;

// modern base64 API
use anyhow::Result;
use base64::engine::general_purpose;
use base64::Engine as _;
use std::panic;

pub fn clipboard_api(api: &mut ApiManager) {
    api.register_api("clipboard.set_text", clipboard_set_text);
    api.register_api("clipboard.get_text", clipboard_get_text);
    api.register_api("clipboard.clear", clipboard_clear);
    api.register_api("clipboard.set_image", clipboard_set_image);
    api.register_api("clipboard.get_image", clipboard_get_image);
}

// Globale Clipboard-Instanz
pub static CLIPBOARD: Lazy<Mutex<Clipboard>> = Lazy::new(|| {
    Clipboard::new()
        .unwrap_or_else(|_| {
            panic!("❌ Clipboard konnte nicht initialisiert werden – keine Systemunterstützung?")
        })
        .into()
});

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ClipboardImage {
    pub width: usize,
    pub height: usize,
    pub data: String,
}

#[api]
fn clipboard_set_text(text: String) -> Result<()> {
    let mut cb = CLIPBOARD
        .lock()
        .map_err(|_| anyhow::anyhow!("Clipboard Lock Error"))?;

    Ok(cb.set_text(text)?)
}

#[api]
fn clipboard_get_text() -> Result<String> {
    let mut cb = CLIPBOARD
        .lock()
        .map_err(|_| anyhow::anyhow!("Clipboard Lock Error"))?;

    Ok(cb.get_text()?)
}

#[api]
fn clipboard_clear() -> Result<()> {
    let mut cb = CLIPBOARD
        .lock()
        .map_err(|_| anyhow::anyhow!("Clipboard Lock Error"))?;

    Ok(cb.clear()?)
}

#[api]
fn clipboard_set_image(width: usize, height: usize, b64_bytes: String) -> Result<bool> {
    let bytes = match general_purpose::STANDARD.decode(&b64_bytes) {
        Ok(b) => b,
        Err(_) => return Ok(false),
    };

    let mut cb = match CLIPBOARD.lock() {
        Ok(c) => c,
        Err(_) => return Ok(false),
    };

    let img = ImageData {
        width,
        height,
        bytes: std::borrow::Cow::Owned(bytes),
    };

    // Panics und normale Fehler auf bool mappen
    match panic::catch_unwind(panic::AssertUnwindSafe(|| cb.set_image(img))) {
        Ok(Ok(())) => Ok(true), // alles gut
        _ => Ok(false),         // Fehler oder Panic
    }
}

#[api]
fn clipboard_get_image() -> Result<ClipboardImage> {
    let mut cb = CLIPBOARD
        .lock()
        .map_err(|_| anyhow::anyhow!("Clipboard Lock Error"))?;
    let result = panic::catch_unwind(panic::AssertUnwindSafe(|| cb.get_image()));

    match result {
        Ok(Ok(img)) => {
            let b64 = general_purpose::STANDARD.encode(img.bytes.as_ref());
            Ok(ClipboardImage {
                width: img.width,
                height: img.height,
                data: b64,
            })
        }
        Ok(Err(e)) => Err(anyhow::anyhow!(
            "Clipboard: Bild konnte nicht gelesen werden: {}",
            e
        )),
        Err(_) => Err(anyhow::anyhow!(
            "Clipboard: interner Panic beim Lesen des Bildes"
        )),
    }
}
