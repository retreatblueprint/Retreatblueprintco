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
