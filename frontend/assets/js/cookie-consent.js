(function () {
  var GA_ID = 'G-QMWDJ8P4HY';
  var KEY = 'gf_cookie_consent';

  function loadGA() {
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA_ID);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  var stored = localStorage.getItem(KEY);
  if (stored === 'accepted') { loadGA(); return; }
  if (stored === 'declined') { return; }

  function showBanner() {
    var el = document.createElement('div');
    el.id = 'cookie-banner';
    el.style.cssText = [
      'position:fixed', 'bottom:0', 'left:0', 'right:0', 'z-index:9999',
      'background:#fff', 'border-top:1px solid #e2e8f0',
      'padding:16px 20px', 'display:flex', 'align-items:center',
      'justify-content:space-between', 'gap:16px', 'flex-wrap:wrap',
      'box-shadow:0 -4px 24px rgba(0,0,0,0.08)',
      'font-family:Manrope,sans-serif', 'font-size:13px', 'color:#334155'
    ].join(';');

    el.innerHTML = [
      '<p style="margin:0;flex:1;min-width:200px">',
        'Използваме бисквитки (cookies) за анализ на трафика чрез Google Analytics.',
        ' Можете да откажете — сайтът работи и без тях.',
      '</p>',
      '<div style="display:flex;gap:8px;flex-shrink:0">',
        '<button id="cookie-decline" style="',
          'padding:8px 16px;border-radius:8px;border:1px solid #cbd5e1;',
          'background:#f8fafc;color:#64748b;font-weight:600;cursor:pointer;font-size:13px',
        '">Само необходими</button>',
        '<button id="cookie-accept" style="',
          'padding:8px 16px;border-radius:8px;border:none;',
          'background:#2563eb;color:#fff;font-weight:700;cursor:pointer;font-size:13px',
        '">Приемам</button>',
      '</div>'
    ].join('');

    document.body.appendChild(el);

    document.getElementById('cookie-accept').addEventListener('click', function () {
      localStorage.setItem(KEY, 'accepted');
      el.remove();
      loadGA();
    });

    document.getElementById('cookie-decline').addEventListener('click', function () {
      localStorage.setItem(KEY, 'declined');
      el.remove();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', showBanner);
  } else {
    showBanner();
  }
})();
