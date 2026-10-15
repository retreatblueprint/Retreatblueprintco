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
