// Copyright 2025-2030 Ari Bermeki @ YellowSiC within The Commons Conservancy
// SPDX-License-Identifier: Apache-2.0
// SPDX-License-Identifier: MIT

/**
 * PyOrion frontend connection bootstrap.
 *
 * Provides a Promise-based `invoke(cmd, args)` API that communicates
 * with the backend via PyOrionConnections (WebSocket).
 *
 * Features:
 *  - Auto reconnect with configurable interval.
 *  - Unique ID mapping for result/error callbacks.
 *  - Automatic cleanup of one-time callbacks.
 *  - Global `window.invoke` helper for command dispatch.
 */
(function () {

  /**
   * Generate a random unique identifier.
   * @returns {number} Unique 32-bit integer.
   */
  function uid() {
    return window.crypto.getRandomValues(new Uint32Array(1))[0];
  }

  /**
   * Register a callback bound to a unique window property.
   * Automatically cleans up if marked as `once`.
   *
   * @param {Function} callback - The callback function.
   * @param {boolean} once - Whether to remove callback after first call.
   * @returns {number} Unique identifier for callback.
   */
function jsonMakeObjectSafe(obj) {
  if (obj === null || obj === undefined) {
    return null;
  }

  // primitive Werte
  if (typeof obj === "string" || typeof obj === "number" || typeof obj === "boolean") {
    return obj;
  }

  // Date / Path -> String
  if (obj instanceof Date) {
    return obj.toISOString();
  }
  if (typeof obj === "object" && obj.constructor && obj.constructor.name === "Path") {
    return String(obj);
  }

  // Buffer / ArrayBuffer / TypedArray -> Base64
  if (obj instanceof ArrayBuffer) {
    return btoa(String.fromCharCode(...new Uint8Array(obj)));
  }
  if (ArrayBuffer.isView(obj)) { // Uint8Array, Float32Array, etc.
    return btoa(String.fromCharCode(...obj));
  }

  // plain Object -> rekursiv
  if (typeof obj === "object" && !Array.isArray(obj)) {
    const safe = {};
    for (const [k, v] of Object.entries(obj)) {
      safe[String(k)] = jsonMakeObjectSafe(v);
    }
    return safe;
  }

  // Array / Set -> rekursiv
  if (Array.isArray(obj) || obj instanceof Set) {
    return Array.from(obj, v => jsonMakeObjectSafe(v));
  }

  // Fallback -> String
  return String(obj);
}


  function transformCallback(callback, once) {
    const identifier = uid();
    const prop = `_${identifier}`;
    Object.defineProperty(window, prop, {
      value: (result) => {
        if (once) Reflect.deleteProperty(window, prop);
        return callback && callback(result);
      },
      writable: false,
      configurable: true
    });
    return identifier;
  }

  /**
   * Invoke a backend command via PyOrionConnections.
   *
   * @param {string} cmd - Command name.
   * @param {any} [args] - Payload arguments (any serializable type).
   * @returns {Promise<any>} Resolves with result of any type, rejects with error.
   */
  function invoke(cmd, args) {
    return new Promise((resolve, reject) => {
      if (!PyOrionConnections.is_connected()) {
        reject(new Error("Socket is not connected or unavailable!"));
        return;
      }
      const py_args = args ?? {};

      const result_id = transformCallback((result) => resolve(result), true);
      const error_id = transformCallback((error) => reject(error), true);

      const message = {
        cmd,
        result_id,
        error_id,
        payload: py_args
      };

      PyOrionConnections.send(message);
    });
  }

PyOrionConnections.on("message", (raw) => {
    try {
      // console.log(raw);
      const data = jsonMakeObjectSafe(JSON.parse(raw));
      const { result_id, error_id, result, error } = data;

      if (result_id) {
        const prop = `_${result_id}`;
        if (window[prop]) window[prop](result);
      }

      if (error_id) {
        const prop = `_${error_id}`;
        if (window[prop]) window[prop](error);
      }
    } catch (err) {
      console.warn("Invalid message received:", raw);
    }
});


  // Expose invoke globally
  window.invoke = invoke;
})();
