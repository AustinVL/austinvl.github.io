// site.js — the only JavaScript on austinvanloon.com: toggles the mobile navigation panel.
(function () {
  var btn = document.querySelector('[data-menu-toggle]');
  var nav = document.getElementById('mobile-nav');
  if (!btn || !nav) return;
  var iconOpen = btn.querySelector('.icon-menu');
  var iconClose = btn.querySelector('.icon-close');
  function setOpen(open) {
    nav.toggleAttribute('data-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (iconOpen) iconOpen.hidden = open;
    if (iconClose) iconClose.hidden = !open;
  }
  btn.addEventListener('click', function () { setOpen(!nav.hasAttribute('data-open')); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  var mq = window.matchMedia('(min-width: 720px)');
  (mq.addEventListener ? mq.addEventListener('change', onChange) : mq.addListener(onChange));
  function onChange(e) { if (e.matches) setOpen(false); }
})();
