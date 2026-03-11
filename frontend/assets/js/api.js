/**
 * Gfinance - API client
 * Base URL and fetch helpers for backend communication
 */

(function () {
  'use strict';

  var API_BASE =
    (typeof document !== 'undefined' &&
      document.documentElement &&
      document.documentElement.getAttribute('data-api-base')) ||
    (typeof window !== 'undefined' &&
    (window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1')
      ? 'http://localhost:8000'
      : '');

  function url(path) {
    path = (path || '').replace(/^\//, '');
    return API_BASE ? API_BASE + '/' + path : '/' + path;
  }

  function pathForHeader(path) {
    var p = (path || '').split('?')[0];
    return p && !p.startsWith('/') ? '/' + p : p || '/';
  }

  async function authHeaders() {
    if (typeof window.getAuthToken === 'function') {
      var t = await window.getAuthToken();
      if (t) return { Authorization: 'Bearer ' + t };
    }
    return {};
  }

  window.api = {
    base: API_BASE,
    url: url,

    get: function (path) {
      return authHeaders().then(function (h) {
        var headers = Object.assign({}, h);
        if (!API_BASE) headers['X-Original-Path'] = pathForHeader(path);
        return fetch(url(path), { credentials: 'include', headers: headers });
      });
    },

    post: function (path, data, timeoutMs) {
      timeoutMs = timeoutMs || 30000;
      return authHeaders().then(function (h) {
        var headers = Object.assign({}, h, { 'Content-Type': 'application/json' });
        if (!API_BASE) headers['X-Original-Path'] = pathForHeader(path);
        var ctrl = typeof AbortController !== 'undefined' ? new AbortController() : null;
        var id = ctrl ? setTimeout(function () { ctrl.abort(); }, timeoutMs) : null;
        return fetch(url(path), {
          method: 'POST',
          headers: headers,
          credentials: 'include',
          body: JSON.stringify(data),
          signal: ctrl ? ctrl.signal : undefined,
        }).finally(function () {
          if (id) clearTimeout(id);
        });
      });
    },

    health: function () {
      return fetch(url('health'), { credentials: 'include' }).then(function (
        res
      ) {
        return res.json();
      });
    },
  };

  /* Optional: ping backend on load (for dev/debug) */
  if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
    window.api.health().catch(function () {});
  }
})();
