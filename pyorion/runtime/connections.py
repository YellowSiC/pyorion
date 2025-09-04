"""WebSocket server connections for the PyOrion runtime.

This module provides the WebSocket server used for communication
between the PyOrion backend and frontend clients. It manages
client registration, message dispatching, and broadcasting responses.
"""

import asyncio
import json
import logging

import websockets
from pydantic import BaseModel
from websockets import ServerConnection

from ..pyinvoke import _event_callbacks, make_callback
from ..runtime import core


def list_commands() -> dict[str, list[str]]:
    """Return a mapping of registered event names -> handler function names."""
    return {key: [f.__name__ for f in funcs] for key, funcs in _event_callbacks.items()}


async def handle_frontend_connections(websocket: ServerConnection) -> None:
    """Handle an individual frontend WebSocket connection."""
    core.connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                payload = json.loads(message)

                if not isinstance(payload, dict):
                    logging.warning("Ignoring non-dict payload: %s", payload)
                    continue

                if all(
                    k in payload for k in ("cmd", "result_id", "error_id", "payload")
                ):
                    cmd = payload["cmd"]

                    # Prüfen, ob Command registriert ist
                    if cmd not in _event_callbacks:
                        logging.error(
                            "No handler registered for event '%s'. Available: %s",
                            cmd,
                            list_commands(),
                        )
                        continue

                    response = await make_callback(
                        cmd,
                        payload["result_id"],
                        payload["error_id"],
                        payload["payload"],
                    )

                    response_msg = (
                        response.model_dump_json(by_alias=True)
                        if isinstance(response, BaseModel)
                        else json.dumps(response)
                    )

                    # Broadcast response to all connected clients
                    await asyncio.gather(
                        *(
                            client.send(response_msg)
                            for client in core.connected_clients
                        )
                    )
                else:
                    logging.warning("Incomplete message keys: %s", payload)
            except json.JSONDecodeError as exc:
                logging.error(
                    "Malformed JSON from %s: %s", websocket.remote_address, exc
                )
            except Exception as exc:
                logging.exception("Unexpected error handling message: %s", exc)
    except websockets.ConnectionClosed:
        logging.info("Client disconnected: %s", websocket.remote_address)
    finally:
        core.connected_clients.discard(websocket)


async def create_websocket_server(host: str = "localhost", port: int = 8765) -> None:
    """Create and run the frontend WebSocket server."""
    logging.info("Starting WebSocket server on ws://%s:%d", host, port)
    logging.info("Registered commands at startup: %s", list_commands())
    async with websockets.serve(handle_frontend_connections, host, port):
        await asyncio.Future()  # Run until externally cancelled
