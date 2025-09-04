use tokio::io::{AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt};

pub async fn handle_client<S>(
    stream: &mut S,
    proxy: crate::utils::FrameEventLoopProxy,
    pending: crate::utils::PendingMap,
) -> tokio::io::Result<()>
where
    S: AsyncRead + AsyncWrite + Unpin,
{
    let mut buf = vec![0u8; 4096];

    loop {
        match stream.read(&mut buf).await {
            Ok(0) => return Ok(()), // Verbindung beendet
            Ok(n) => {
                let request_str = match String::from_utf8(buf[..n].to_vec()) {
                    Ok(s) => s,
                    Err(_) => continue,
                };

                let req: crate::api_manager::ApiRequest = match serde_json::from_str(&request_str) {
                    Ok(req) => req,
                    Err(e) => {
                        eprintln!("[platform] JSON parse error: {:?}", e);
                        continue;
                    }
                };

                let (tx, rx) = tokio::sync::oneshot::channel();
                {
                    let mut map = pending.lock().unwrap();
                    map.insert(req.0.clone(), tx);
                }

                let _ = proxy.send_event(crate::utils::UserEvent::Request(req.clone()));

                match rx.await {
                    Ok(resp) => {
                        let response_json = serde_json::to_string(&resp)?;
                        stream.write_all(response_json.as_bytes()).await?;
                        stream.flush().await?;
                    }
                    Err(_) => {
                        let error_response = crate::api_manager::ApiResponse(
                            req.0,
                            500,
                            "Internal server error".to_string(),
                            serde_json::json!(null),
                        );
                        let response_json = serde_json::to_string(&error_response)?;
                        stream.write_all(response_json.as_bytes()).await?;
                        stream.flush().await?;
                    }
                }
            }
            Err(e) => {
                eprintln!("[platform] Read error: {:?}", e);
                return Err(e);
            }
        }
    }
}
