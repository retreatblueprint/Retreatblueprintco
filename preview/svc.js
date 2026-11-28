(function () {
  // Service pages: one photo stage stays in place; each stop pins over it while its own photo fades in.
  // Same behaviour as the homepage preview, for any number of stops.
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = document.querySelector('.zworld'), st = W.querySelector('.zstick');
  var imgs = [].slice.call(st.querySelectorAll('.svimg'));
  var heroShade = st.querySelector('.zshade--hero'), shade = st.querySelector('.svshade');
  var s1 = W.querySelector('.zs1'), cp = W.querySelector('.zcopy');
  var stops = [].slice.call(W.querySelectorAll(':scope > .svstop, :scope > .svflow')).map(function (el) {
    var wrap = el.querySelector(':scope > .wrap');
    return { el: el, flow: el.classList.contains('svflow'), wrap: wrap, kids: [].slice.call(wrap.children) };
  });
  var c = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; }, ease = function (t) { return t * t * (3 - 2 * t); };
  var seg = function (y, a, b) { return ease(c((y - a) / (b - a))); };
  var heroOut = 0;
  function layout() {
    var vh = window.innerHeight; heroOut = vh * .3;
    var prevOut = 0;
    stops.forEach(function (sp, i) {
      sp.el.style.marginTop = '0px';
      var natural = sp.el.offsetTop;
      sp.el.style.marginTop = ((i === 0 ? 0 : prevOut) - natural) + 'px';
      var top = sp.el.offsetTop, hgt = sp.el.offsetHeight;
      if (i === 0) { sp.a = top + vh * .06; sp.b = top + vh * .6; }
      else { sp.a = prevOut + vh * .05; sp.b = prevOut + vh * .65; }
      if (sp.flow) sp.out = top + hgt - vh * .55;                       // the calm-scroll card hands over as its end comes up
      else sp.out = i === stops.length - 1 ? Infinity : top + hgt - vh * 1.45;
      if (!sp.flow) {
        var mk = sp.el.querySelector(':scope > .zsnap');
        if (!mk) { mk = document.createElement('div'); mk.className = 'zsnap'; mk.setAttribute('aria-hidden', 'true'); sp.el.appendChild(mk); }
        mk.style.top = (sp.b + vh * .08 - top) + 'px';
      }
      prevOut = sp.out;
    });
  }
  function slide(kids, y, a, b, fo) {
    kids.forEach(function (el, i) {
      var n = kids.length, s0 = a + (b - a) * i * .12, k = seg(y, s0, b - (b - a) * (n - 1 - i) * .04), v = k * (1 - fo);
      var landed = k >= 1 && !(fo > 0);
      el.style.opacity = landed ? '1' : v;
      el.style.transform = landed ? 'none' : 'translateX(' + (-90 * (1 - k)) + 'px) translateY(' + (-24 * fo) + 'px)';
    });
  }
  function frame() {
    ticking = false;
    var vh = window.innerHeight, y = -W.getBoundingClientRect().top;
    if (y > W.offsetHeight) return;
    var h = c(y / heroOut);
    cp.style.opacity = 1 - h; cp.style.transform = 'translateY(' + (-70 * h) + 'px)'; heroShade.style.opacity = 1 - h;
    var kin = stops.map(function (sp) { return seg(y, sp.a, sp.b); });
    var kout = stops.map(function (sp) { return sp.out === Infinity ? 0 : seg(y, sp.out, sp.out + vh * .3); });
    stops.forEach(function (sp, i) {
      if (sp.flow) return;
      slide(sp.kids, y, sp.a, sp.b, kout[i]);
      sp.wrap.style.visibility = kin[i] * (1 - kout[i]) < .01 ? 'hidden' : '';
    });
    // photos: hero photo drifts in as the first stop arrives; each later stop's photo fades in over the last
    if (!reduce) imgs[0].style.transform = 'scale(' + (1 + .45 * kin[0] + .15 * (kin[1] || 0)) + ')';
    for (var n = 1; n < imgs.length; n++) {
      var kk = kin[n - 1] || 0, next = kin[n] || 0;
      imgs[n].style.opacity = kk;
      if (!reduce) imgs[n].style.transform = 'scale(' + (1.3 - .3 * kk + .22 * next) + ')';
    }
    shade.style.opacity = kin[0];
  }
  // voice notes
  var audios = [];
  var PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>';
  var PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/></svg>';
  var fmt = function (s) { s = Math.max(0, Math.round(s || 0)); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };
  [].slice.call(document.querySelectorAll('.vnote')).forEach(function (p) {
    var btn = p.querySelector('.vplay'), bar = p.querySelector('.vbar i'), time = p.querySelector('.vtime'), label = btn.getAttribute('aria-label');
    var a = new Audio(p.dataset.src); a.preload = 'metadata'; audios.push(a);
    btn.addEventListener('click', function () { if (a.paused) { audios.forEach(function (o) { if (o !== a) o.pause(); }); a.play().catch(function () {}); } else a.pause(); });
    a.addEventListener('play', function () { btn.innerHTML = PAUSE; btn.setAttribute('aria-label', label.replace('Play', 'Pause')); });
    a.addEventListener('pause', function () { btn.innerHTML = PLAY; btn.setAttribute('aria-label', label); });
    a.addEventListener('timeupdate', function () { if (a.duration) { bar.style.width = (a.currentTime / a.duration * 100) + '%'; time.textContent = fmt(a.currentTime) + ' / ' + fmt(a.duration); } });
    a.addEventListener('ended', function () { bar.style.width = '0'; time.textContent = fmt(a.duration); });
  });
  // in-page links land where a stop has fully arrived
  function landing(id) {
    var el = document.getElementById(id); if (!el) return null;
    for (var i = 0; i < stops.length; i++) if (stops[i].el === el || stops[i].el.contains(el)) {
      return stops[i].flow ? el.getBoundingClientRect().top + window.pageYOffset + parseFloat(getComputedStyle(stops[i].el).paddingTop) - 90 : W.offsetTop + stops[i].b + window.innerHeight * .08;
    }
    return el.getBoundingClientRect().top + window.pageYOffset - 80;
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="#"]'); if (!a) return;
    var raw = a.getAttribute('href') || ''; var url = new URL(raw.charAt(0) === '#' ? location.pathname + location.search + raw : a.href, location.href); if (url.pathname !== location.pathname || !url.hash) return;
    var y = landing(decodeURIComponent(url.hash.slice(1))); if (y === null) return;
    e.preventDefault(); history.replaceState(null, '', location.pathname + location.search + url.hash);
    window.scrollTo({ top: y, behavior: 'auto' });
  });
  if (location.hash) window.addEventListener('load', function () { var y = landing(location.hash.slice(1)); if (y !== null) window.scrollTo(0, y); });
  if (reduce) document.documentElement.classList.add('zstatic');
  var ticking = false;
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  layout(); frame();
  window.addEventListener('scroll', req, { passive: true });
  var lastW = window.innerWidth, lastH = window.innerHeight;
  window.addEventListener('resize', function () {
    var w = window.innerWidth, h = window.innerHeight;
    if (w === lastW && Math.abs(h - lastH) < 160) { req(); return; }
    lastW = w; lastH = h; layout(); req();
  });
  window.addEventListener('load', function () { layout(); req(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { layout(); req(); });
  if (window.ResizeObserver) { var roW = s1.offsetWidth, ro = new ResizeObserver(function () { if (s1.offsetWidth !== roW) { roW = s1.offsetWidth; layout(); } req(); }); ro.observe(s1);
    // opening an FAQ answer makes the calm-scroll card taller: re-time what comes after it
    stops.forEach(function (sp) { if (!sp.flow) return; var lastH = sp.el.offsetHeight; new ResizeObserver(function () { if (sp.el.offsetHeight !== lastH) { lastH = sp.el.offsetHeight; layout(); req(); } }).observe(sp.el); }); }
})();
