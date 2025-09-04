"""Runtime management for PyOrion.

This module defines functions to launch, manage, and gracefully
terminate the PyOrion runtime, including background tasks,
subprocesses, and WebSocket communication.
"""

import asyncio
from collections.abc import Coroutine
from multiprocessing import get_context
from multiprocessing.context import SpawnProcess
from pathlib import Path

from pyorion.types import WindowOptions

from .._pyorion import create_webframe
from . import core
from .connections import create_websocket_server
from .runtime_handle import eventloop_sender


shutdown_event = None  # Global shutdown event shared across the runtime


def locate_project_folder(folder_name: str) -> Path | None:
    """Locate a folder within the current working directory.

    :param folder_name: Name of the folder to search for.
    :type folder_name: str
    :return: Path to the folder if found, otherwise None.
    :rtype: Path | None
    """
    start_path = Path.cwd()
    base = Path(start_path).resolve()
    candidate = base / folder_name
    return candidate if candidate.exists() else None


def launch_background_task(coro: Coroutine) -> asyncio.Task:
    """Start an asyncio task and track it in the background task set.

    :param coro: Coroutine to be scheduled as a task.
    :type coro: Coroutine
    :return: The created asyncio task.
    :rtype: asyncio.Task
    """
    task = asyncio.create_task(coro)
    core.background_tasks.add(task)
    task.add_done_callback(core.background_tasks.discard)
    return task


async def cancel_all_tasks(loop: asyncio.AbstractEventLoop) -> None:
    """Cancel all running asyncio tasks and ensure a clean shutdown.

    :param loop: The asyncio event loop to operate on.
    :type loop: asyncio.AbstractEventLoop
    """
    for task in list(core.background_tasks):
        task.cancel()
    pending = [
        t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task(loop)
    ]
    for task in pending:
        task.cancel()
    results = await asyncio.gather(*pending, return_exceptions=True)
    for r in results:
        if isinstance(r, Exception) and not isinstance(r, asyncio.CancelledError):
            print(f"Task raised during shutdown: {r!r}")


def terminate_process_safely(proc: SpawnProcess) -> None:
    """Terminate a spawned process gracefully, with fallback to kill.

    :param proc: The process to terminate.
    :type proc: multiprocessing.context.SpawnProcess
    """
    proc.join(3.0)
    if proc.is_alive():
        proc.terminate()
        proc.join(2.0)
    if proc.is_alive():
        proc.kill()
        proc.join()


async def run_native_runtime(
    init_options: WindowOptions, host: str = "localhost", port: int = 8080
) -> None:
    """Start the native runtime environment including the WebFrame process and servers.

    This function manages the lifecycle of the WebFrame subprocess as well
    as the asyncio-based background servers (WebSocket and event loop sender).

    A multiprocessing ``Manager`` is used here to create a shared
    synchronization primitive (``Event``). Unlike a normal
    ``threading.Event`` or ``asyncio.Event``, the manager-provided ``Event``
    can be safely shared across processes. This allows the subprocess
    (WebFrame) and the parent process to communicate shutdown signals
    reliably, ensuring coordinated termination.

    :param init_options: Window configuration options serialized into JSON and passed to the WebFrame process.
    :type init_options: WindowOptions
    :param host: Host address for the WebSocket server.
    :type host: str, optional
    :param port: Port number for the WebSocket server.
    :type port: int, optional
    """
    loop = asyncio.get_running_loop()

    # Start background tasks
    launch_background_task(create_websocket_server(host, port))
    launch_background_task(eventloop_sender())

    ctx = get_context("spawn")
    with ctx.Manager() as manager:
        close_event = manager.Event()
        config = init_options.model_dump_json(by_alias=True)

        global shutdown_event
        shutdown_event = close_event
        name_pipe = "pyframe_pipe"
        proc = ctx.Process(
            target=create_webframe,
            args=(config, host, port, name_pipe, close_event),
            daemon=False,
        )
        proc.start()

        try:
            # Wait until the subprocess signals shutdown via the shared Event
            await loop.run_in_executor(None, close_event.wait)
        finally:
            await loop.run_in_executor(None, lambda: terminate_process_safely(proc))

    await cancel_all_tasks(loop)
