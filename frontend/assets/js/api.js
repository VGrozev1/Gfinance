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
    path = path.replace(/^\//, '');
    return API_BASE ? API_BASE + '/' + path : '/' + path;
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
        return fetch(url(path), { credentials: 'include', headers: h });
      });
    },

    post: function (path, data) {
      return authHeaders().then(function (h) {
        var headers = Object.assign({}, h, { 'Content-Type': 'application/json' });
        return fetch(url(path), {
          method: 'POST',
          headers: headers,
          credentials: 'include',
          body: JSON.stringify(data),
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
