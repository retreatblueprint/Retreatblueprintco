(function () {
  // One stage of photos stays in place while each section pins over it in turn.
  // Lagoon (hero) → cabins from above (framework) → cabin close-up (proof) → pool view (services)
  // → open-air lounge (how we start) → glass room (about) → dock at dusk (close).
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = document.querySelector('.zworld'), st = W.querySelector('.zstick');
  var q = function (sel, root) { return (root || document).querySelector(sel); };
  var img = [null, q('.z1', st), q('.z2', st), q('.z3', st), q('.z4', st), q('.z5', st), q('.z6', st)];
  var shade = { hero: q('.zshade--hero', st), water: q('.zshade--water', st), cabins: q('.zshade--cabins', st), pool: q('.zshade--pool', st), warm: q('.zshade--warm', st) };
  var s1 = q('.zs1', W), cp = q('.zcopy', W);
  // stops in order: framework, proof, services, how we start, about, close
  var stops = ['.zs2', '.zs3', '.zs4', '.zs5', '.zs6', '.zs7'].map(function (sel) {
    var el = q(sel, W);
    return { el: el, wrap: el.querySelector(':scope > .wrap'), kids: [].slice.call(el.querySelectorAll(':scope > .wrap > *')) };
  });
  var bands = [].slice.call(document.querySelectorAll('.zwin')), secs = [].slice.call(document.querySelectorAll('[data-zoom]'));
  var IW = 1600, IH = 927, FX = .75, FY = .605, ZMID = 3.6, ZEND = 8;   // the cabins' spot in the lagoon photo
  var c = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; }, ease = function (t) { return t * t * (3 - 2 * t); };
  var seg = function (y, a, b) { return ease(c((y - a) / (b - a))); };
  var heroOut = 0;
  function layout() {
    var w = st.clientWidth, h = st.clientHeight, s = Math.max(w / IW, h / IH), rw = IW * s, rh = IH * s;
    img[1].style.transformOrigin = ((w - rw) * .75 + FX * rw) + 'px ' + ((h - rh) * .5 + FY * rh) + 'px';
    var vh = window.innerHeight; heroOut = vh * .3;
    var prevOut = 0;
    stops.forEach(function (sp, i) {
      sp.el.style.marginTop = '0px';
      var natural = sp.el.offsetTop;
      // framework starts at the very top; every later stop is already pinned when the one before it starts to leave
      sp.el.style.marginTop = ((i === 0 ? 0 : prevOut) - natural) + 'px';
      var top = sp.el.offsetTop, hgt = sp.el.offsetHeight;
      if (i === 0) { sp.a = top + vh * .06; sp.b = top + vh * .6; }
      else { sp.a = prevOut + vh * .05; sp.b = prevOut + vh * .65; }
      sp.out = i === stops.length - 1 ? Infinity : top + hgt - vh * 1.45;
      prevOut = sp.out;
    });
  }
  function slide(kids, y, a, b, fo) {
    kids.forEach(function (el, i) {
      var n = kids.length, s0 = a + (b - a) * i * .12, k = seg(y, s0, b - (b - a) * (n - 1 - i) * .04), v = k * (1 - fo);
      var landed = k >= 1 && !(fo > 0);
      el.style.opacity = landed ? '1' : v;
      // once landed, no transform, so frosted glass can blur the photo behind it
      el.style.transform = landed ? 'none' : 'translateX(' + (-90 * (1 - k)) + 'px) translateY(' + (-24 * fo) + 'px)';
    });
  }
  function frame() {
    ticking = false;
    var vh = window.innerHeight, y = -W.getBoundingClientRect().top;
    if (y < W.offsetHeight) {
      var h = c(y / heroOut);
      cp.style.opacity = 1 - h; cp.style.transform = 'translateY(' + (-70 * h) + 'px)'; shade.hero.style.opacity = 1 - h;
      var kin = stops.map(function (sp) { return seg(y, sp.a, sp.b); });
      var kout = stops.map(function (sp) { return sp.out === Infinity ? 0 : seg(y, sp.out, sp.out + vh * .3); });
      stops.forEach(function (sp, i) {
        slide(sp.kids, y, sp.a, sp.b, kout[i]);
        sp.wrap.style.visibility = kin[i] * (1 - kout[i]) < .01 ? 'hidden' : '';
      });
      // each stop's photo fades in over the last; the outgoing photo keeps drifting closer
      if (!reduce) img[1].style.transform = 'scale(' + (1 + (ZMID - 1) * kin[0] + (ZEND - ZMID) * seg(y, stops[0].out, stops[1].b)) + ')';
      for (var n = 2; n <= 6; n++) {
        var kk = kin[n - 1], next = kin[n] || 0;
        img[n].style.opacity = kk;
        if (!reduce) img[n].style.transform = 'scale(' + (1.3 - .3 * kk + .22 * next) + ')';
      }
      shade.water.style.opacity = seg(y, stops[0].a - vh * .06, stops[0].b - vh * .1) * (1 - kout[0]);
      shade.cabins.style.opacity = kin[1] * (1 - kin[2]);
      shade.pool.style.opacity = kin[2] * (1 - kin[3]);
      shade.warm.style.opacity = kin[3];
    }
    if (reduce) return;
    bands.forEach(function (b) {
      var r = b.getBoundingClientRect(); if (r.bottom < 0 || r.top > vh) return;
      var k = ease(c((vh - r.top) / (vh * .85)));
      b.style.setProperty('--ix', (18 * (1 - k)) + '%'); b.style.setProperty('--iy', (10 * (1 - k)) + '%');
      b.style.setProperty('--rr', (28 * (1 - k)) + 'px'); b.style.setProperty('--zs', 1.25 - .25 * k);
    });
    secs.forEach(function (s) {
      var r = s.getBoundingClientRect(); if (r.top > vh || r.bottom < 0) return;
      var k = ease(c((vh - r.top) / (vh * .6)));
      s.style.transform = k < 1 ? 'scale(' + (.93 + .07 * k) + ')' : ''; s.style.borderRadius = k < 1 ? (30 * (1 - k)) + 'px' : '';
    });
  }
  // voice notes in the proof stop
  var players = [].slice.call(document.querySelectorAll('.vnote')), audios = [];
  var PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>';
  var PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/></svg>';
  var fmt = function (s) { s = Math.max(0, Math.round(s || 0)); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };
  players.forEach(function (p) {
    var btn = p.querySelector('.vplay'), bar = p.querySelector('.vbar i'), time = p.querySelector('.vtime'), label = btn.getAttribute('aria-label');
    var a = new Audio(p.dataset.src); a.preload = 'metadata'; audios.push(a);
    btn.addEventListener('click', function () { if (a.paused) { audios.forEach(function (o) { if (o !== a) o.pause(); }); a.play().catch(function () {}); } else a.pause(); });
    a.addEventListener('play', function () { btn.innerHTML = PAUSE; btn.setAttribute('aria-label', label.replace('Play', 'Pause')); });
    a.addEventListener('pause', function () { btn.innerHTML = PLAY; btn.setAttribute('aria-label', label); });
    a.addEventListener('timeupdate', function () { if (a.duration) { bar.style.width = (a.currentTime / a.duration * 100) + '%'; time.textContent = fmt(a.currentTime) + ' / ' + fmt(a.duration); } });
    a.addEventListener('ended', function () { bar.style.width = '0'; time.textContent = fmt(a.duration); });
  });
  // "Read my story" opens the full About text
  var dlg = document.querySelector('.astory'), rd = document.querySelector('.aread');
  if (dlg && rd) {
    rd.addEventListener('click', function () { if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); });
    dlg.querySelector('.aclose').addEventListener('click', function () { if (dlg.close) dlg.close(); else dlg.removeAttribute('open'); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg && dlg.close) dlg.close(); });
  }
  // "Read full testimonial" opens the owner's complete testimonial
  [].slice.call(document.querySelectorAll('.tread')).forEach(function (b) {
    var d = document.getElementById(b.dataset.open); if (!d) return;
    b.addEventListener('click', function () { if (d.showModal) d.showModal(); else d.setAttribute('open', ''); });
    d.querySelector('.aclose').addEventListener('click', function () { if (d.close) d.close(); else d.removeAttribute('open'); });
    d.addEventListener('click', function (e) { if (e.target === d && d.close) d.close(); });
  });
  if (reduce) document.documentElement.classList.add('zstatic');
  var ticking = false;
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  layout(); frame();
  window.addEventListener('scroll', req, { passive: true });
  // phones: the address bar showing/hiding changes the height only; don't re-time the page mid-scroll for that
  var lastW = window.innerWidth, lastH = window.innerHeight;
  window.addEventListener('resize', function () {
    var w = window.innerWidth, h = window.innerHeight;
    if (w === lastW && Math.abs(h - lastH) < 160) { req(); return; }
    lastW = w; lastH = h; layout(); req();
  });
  window.addEventListener('load', function () { layout(); req(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { layout(); req(); });
  if (window.ResizeObserver) { var roW = s1.offsetWidth, ro = new ResizeObserver(function () { if (s1.offsetWidth !== roW) { roW = s1.offsetWidth; layout(); } req(); }); ro.observe(s1); }
})();
