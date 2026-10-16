// Phone and tablet menu, shared by every page
(function () {
  document.querySelectorAll('[data-menu]').forEach(function (nav) {
    var btn = nav.querySelector('[data-menu-toggle]');
    if (!btn) return;
    function setOpen(open) {
      nav.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }
    btn.addEventListener('click', function () { setOpen(!nav.classList.contains('menu-open')); });
    nav.querySelectorAll('[data-menu-links] a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
    document.addEventListener('click', function (e) { if (!nav.contains(e.target)) setOpen(false); });
  });
})();

// Services drop-down: click to open, closes on outside click or Esc; hover opens it on desktop
(function () {
  var hover = window.matchMedia('(hover: hover) and (min-width: 961px)');
  document.querySelectorAll('[data-dd]').forEach(function (dd) {
    var btn = dd.querySelector('.dd-btn'), t;
    function set(open) { dd.classList.toggle('open', open); btn.setAttribute('aria-expanded', open ? 'true' : 'false'); }
    btn.addEventListener('click', function (e) { e.stopPropagation(); clearTimeout(t); set(hover.matches ? true : !dd.classList.contains('open')); }); // on desktop hover already opened it, so a click keeps it open
    dd.addEventListener('mouseenter', function () { if (hover.matches) { clearTimeout(t); set(true); } });
    dd.addEventListener('mouseleave', function () { if (hover.matches) { t = setTimeout(function () { set(false); }, 180); } });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) set(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  });
})();

// WhatsApp button, bottom right on every page
(function () {
  if (document.querySelector('.wa-float')) return;
  var a = document.createElement('a');
  a.className = 'wa-float';
  a.href = 'https://wa.me/16479702759?text=' + encodeURIComponent("Hi Shila, I found Retreat Blueprint Co. and I'd like to chat about my retreat.");
  a.target = '_blank';
  a.rel = 'noopener';
  a.setAttribute('aria-label', 'Message Shila on WhatsApp');
  a.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.6-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.6-.3z"/></svg><span>WhatsApp</span>';
  document.body.appendChild(a);
  var t = document.querySelector('[data-menu-toggle]');
  if (t) new MutationObserver(function () { document.body.classList.toggle('menu-open', t.getAttribute('aria-expanded') === 'true'); }).observe(t, { attributes: true, attributeFilter: ['aria-expanded'] });
})();
