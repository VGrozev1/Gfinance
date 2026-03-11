/**
 * Gfinance - Main JavaScript
 * Mobile menu, smooth scroll, and shared helpers
 */

(function () {
  'use strict';

  /* --- Mobile menu (event delegation - works even if DOM not ready at init) --- */
  function getNav() {
    return {
      menu: document.querySelector('[data-nav-menu]'),
      overlay: document.querySelector('[data-nav-overlay]'),
    };
  }

  function openNav() {
    var nav = getNav();
    if (nav.menu) nav.menu.classList.add('is-open');
    if (nav.overlay) nav.overlay.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  function closeNav() {
    var nav = getNav();
    if (nav.menu) nav.menu.classList.remove('is-open');
    if (nav.overlay) nav.overlay.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  function toggleNav() {
    var menu = document.querySelector('[data-nav-menu]');
    if (menu && menu.classList.contains('is-open')) {
      closeNav();
    } else {
      openNav();
    }
  }

  function initNav() {
    document.body.addEventListener('click', function (e) {
      var toggle = e.target && e.target.closest && e.target.closest('[data-nav-toggle]');
      if (toggle) {
        e.preventDefault();
        e.stopPropagation();
        toggleNav();
      }
    });
    var overlay = document.querySelector('[data-nav-overlay]');
    if (overlay) overlay.addEventListener('click', closeNav);
    var menu = document.querySelector('[data-nav-menu]');
    if (menu) {
      menu.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', closeNav);
      });
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNav);
  } else {
    initNav();
  }

  /* --- Hide login link when user is logged in --- */
  function isLoggedIn() {
    try {
      if (window.supabase && typeof window.supabase.auth.getSession === 'function') {
        return window.supabase.auth.getSession().then(function(r) {
          return !!(r.data && r.data.session);
        });
      }
      var keys = Object.keys(localStorage);
      for (var i = 0; i < keys.length; i++) {
        var k = keys[i];
        if (k.indexOf('sb-') === 0 && (k.indexOf('-auth-token') !== -1 || k.indexOf('auth-token') !== -1)) {
          var raw = localStorage.getItem(k);
          if (!raw) continue;
          var data = JSON.parse(raw);
          var token = data && (data.access_token || (data.currentSession && data.currentSession.access_token));
          return Promise.resolve(!!token);
        }
      }
    } catch (e) {}
    return Promise.resolve(false);
  }
  function updateNavLoginVisibility() {
    var loginLinks = document.querySelectorAll('[data-nav-login]');
    if (loginLinks.length === 0) return;
    isLoggedIn().then(function(loggedIn) {
      loginLinks.forEach(function(el) {
        el.style.display = loggedIn ? 'none' : '';
        if (loggedIn) {
          el.setAttribute('aria-hidden', 'true');
        } else {
          el.removeAttribute('aria-hidden');
        }
      });
    });
  }
  window.updateNavLoginVisibility = updateNavLoginVisibility;
  function runNavLoginUpdate() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        updateNavLoginVisibility();
        setTimeout(updateNavLoginVisibility, 300);
      });
    } else {
      updateNavLoginVisibility();
      setTimeout(updateNavLoginVisibility, 300);
    }
  }
  runNavLoginUpdate();
  if (window.auth && typeof window.auth.onAuthStateChange === 'function') {
    window.auth.onAuthStateChange(function() {
      updateNavLoginVisibility();
    });
  }

  /* --- Smooth scroll for anchor links --- */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* --- Toast / showMessage helper --- */
  window.showMessage = function (text, type) {
    type = type || 'info';
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast toast--' + type;
    toast.textContent = text;
    toast.setAttribute('role', 'alert');
    document.body.appendChild(toast);

    requestAnimationFrame(function () {
      toast.classList.add('is-visible');
    });

    setTimeout(function () {
      toast.classList.remove('is-visible');
      setTimeout(function () {
        toast.remove();
      }, 300);
    }, 3500);
  };
})();
