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

  /* --- Floating contact CTAs (mobile only, not on booking_confirmed) --- */
  function initFloatingCTA() {
    var path = window.location.pathname;
    if (path.indexOf('/booking_confirmed') !== -1) return;

    var BTNS = [
      { href: 'tel:+359888152181',              bg: '#2563eb', shadow: 'rgba(37,99,235,0.4)',  label: 'Обади се на Gfinance',    icon: '<span class="material-symbols-outlined" style="font-size:26px;line-height:1">call</span>' },
      { href: 'https://wa.me/359888152181',      bg: '#25D366', shadow: 'rgba(37,211,102,0.4)', label: 'WhatsApp на Gfinance',     icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="#fff"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>' },
      { href: 'viber://chat?number=%2B359888152181', bg: '#7360F2', shadow: 'rgba(115,96,242,0.4)', label: 'Viber на Gfinance', icon: '<img src="/assets/images/viber-icon.svg" width="26" height="26" alt="" style="filter:brightness(0) invert(1)">' },
    ];

    var wrap = document.createElement('div');
    wrap.style.cssText = 'position:fixed;bottom:24px;right:20px;z-index:900;display:flex;flex-direction:column-reverse;gap:10px;align-items:center';

    BTNS.forEach(function(def) {
      var btn = document.createElement('a');
      btn.href = def.href;
      if (def.href.indexOf('wa.me') !== -1) { btn.target = '_blank'; btn.rel = 'noopener noreferrer'; }
      btn.setAttribute('aria-label', def.label);
      btn.style.cssText = [
        'width:52px', 'height:52px', 'border-radius:50%',
        'background:' + def.bg, 'color:#fff',
        'display:flex', 'align-items:center', 'justify-content:center',
        'box-shadow:0 4px 14px ' + def.shadow,
        'text-decoration:none', 'transition:transform 0.15s,box-shadow 0.15s'
      ].join(';');
      btn.innerHTML = def.icon;
      btn.addEventListener('mouseenter', function() { btn.style.transform = 'scale(1.08)'; });
      btn.addEventListener('mouseleave', function() { btn.style.transform = ''; });
      wrap.appendChild(btn);
    });

    var mq = window.matchMedia('(max-width:767px)');
    function toggle(e) { wrap.style.display = e.matches ? 'flex' : 'none'; }
    toggle(mq);
    if (mq.addEventListener) mq.addEventListener('change', toggle);
    else mq.addListener(toggle);
    document.body.appendChild(wrap);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFloatingCTA);
  } else {
    initFloatingCTA();
  }

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
