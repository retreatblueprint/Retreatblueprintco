(function () {
  // One photo stays in place while three pinned screens play over it:
  // hero → zoom to the cabins with the framework → zoom in close with the guest journey.
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = document.querySelector('.zworld'), st = W.querySelector('.zstick'),
      z1 = st.querySelector('.z1'), z2 = st.querySelector('.z2'), z3 = st.querySelector('.z3'), sp = st.querySelector('.zshade--pool'),
      sh = st.querySelector('.zshade--hero'), sw = st.querySelector('.zshade--water'), sc = st.querySelector('.zshade--cabins'),
      s1 = W.querySelector('.zs1'), cp = W.querySelector('.zcopy'),
      s2 = W.querySelector('.zs2'), f2 = s2.querySelector(':scope > .wrap'), k2 = [].slice.call(s2.querySelectorAll(':scope > .wrap > *')),
      s3 = W.querySelector('.zs3'), f3 = s3.querySelector(':scope > .wrap'), k3 = [].slice.call(s3.querySelectorAll(':scope > .wrap > *')),
      s4 = W.querySelector('.zs4'), f4 = s4.querySelector(':scope > .wrap'), k4 = [].slice.call(s4.querySelectorAll(':scope > .wrap > *'));
  var bands = [].slice.call(document.querySelectorAll('.zwin')), secs = [].slice.call(document.querySelectorAll('[data-zoom]'));
  var IW = 1600, IH = 927, FX = .75, FY = .605, ZMID = 3.6, ZEND = 8;   // the cabins' spot in the lagoon photo
  var c = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; }, ease = function (t) { return t * t * (3 - 2 * t); };
  var seg = function (y, a, b) { return ease(c((y - a) / (b - a))); };
  var A = {};
  function layout() {
    var w = st.clientWidth, h = st.clientHeight, s = Math.max(w / IW, h / IH), rw = IW * s, rh = IH * s;
    z1.style.transformOrigin = ((w - rw) * .75 + FX * rw) + 'px ' + ((h - rh) * .5 + FY * rh) + 'px';
    var vh = window.innerHeight;
    s2.style.marginTop = (-s1.offsetHeight) + 'px';               // framework layer starts at the top, already pinned
    var t2 = s2.offsetTop, h2 = s2.offsetHeight, out2 = t2 + h2 - vh * 1.45;
    s3.style.marginTop = (out2 - (t2 + h2)) + 'px';                // journey layer is pinned by the time the framework leaves
    A = { heroOut: vh * .3,
          in2a: t2 + vh * .06, in2b: t2 + vh * .6,                 // zoom 1 and framework land together
          out2a: out2, out2b: out2 + vh * .3,
          zoom2b: out2 + vh * .7,                                  // zoom 2 into the cabins
          in3a: out2 + vh * .05, in3b: out2 + vh * .65 };           // journey lands as zoom 2 lands
    var t3 = s3.offsetTop, h3 = s3.offsetHeight, out3 = t3 + h3 - vh * 1.45;
    s4.style.marginTop = (out3 - (t3 + h3)) + 'px';                // services layer is pinned by the time the journey leaves
    A.out3a = out3; A.out3b = out3 + vh * .3;
    A.in4a = out3 + vh * .05; A.in4b = out3 + vh * .65;            // step inside: the pool view and the services land together
  }
  function slide(kids, y, a, b, fo) {
    kids.forEach(function (el, i) {
      var n = kids.length, s0 = a + (b - a) * i * .12, k = seg(y, s0, b - (b - a) * (n - 1 - i) * .04), v = k * (1 - (fo || 0));
      el.style.opacity = v;
      el.style.transform = 'translateX(' + (-90 * (1 - k)) + 'px) translateY(' + (-24 * (fo || 0)) + 'px)';
    });
  }
  function frame() {
    ticking = false;
    var vh = window.innerHeight, y = -W.getBoundingClientRect().top;
    if (y < W.offsetHeight) {
      var h = c(y / A.heroOut);
      cp.style.opacity = 1 - h; cp.style.transform = 'translateY(' + (-70 * h) + 'px)'; sh.style.opacity = 1 - h;
      var i2 = seg(y, A.in2a, A.in2b), o2 = seg(y, A.out2a, A.out2b), x = seg(y, A.in3a, A.in3b), zz = seg(y, A.out2a, A.zoom2b);
      if (!reduce) {
        z1.style.transform = 'scale(' + (1 + (ZMID - 1) * i2 + (ZEND - ZMID) * zz) + ')';
      }
      z2.style.opacity = x;
      sw.style.opacity = seg(y, A.in2a - vh * .06, A.in2b - vh * .1) * (1 - o2);
      slide(k2, y, A.in2a, A.in2b, o2);
      f2.style.visibility = i2 * (1 - o2) < .01 ? 'hidden' : '';
      var o3 = seg(y, A.out3a, A.out3b), x4 = seg(y, A.in4a, A.in4b);
      slide(k3, y, A.in3a, A.in3b, o3);
      f3.style.visibility = x * (1 - o3) < .01 ? 'hidden' : '';
      z3.style.opacity = x4; sp.style.opacity = x4; sc.style.opacity = x * (1 - x4);
      if (!reduce) { z3.style.transform = 'scale(' + (1.3 - .3 * x4) + ')'; z2.style.transform = 'scale(' + (1.35 - .35 * x + .25 * x4) + ')'; }
      slide(k4, y, A.in4a, A.in4b, 0);
      f4.style.visibility = x4 < .01 ? 'hidden' : '';
    }
    if (reduce) return;
    bands.forEach(function (b) {
      var q = b.getBoundingClientRect(); if (q.bottom < 0 || q.top > vh) return;
      var k = ease(c((vh - q.top) / (vh * .85)));
      b.style.setProperty('--ix', (18 * (1 - k)) + '%'); b.style.setProperty('--iy', (10 * (1 - k)) + '%');
      b.style.setProperty('--rr', (28 * (1 - k)) + 'px'); b.style.setProperty('--zs', 1.25 - .25 * k);
    });
    secs.forEach(function (s) {
      var q = s.getBoundingClientRect(); if (q.top > vh || q.bottom < 0) return;
      var k = ease(c((vh - q.top) / (vh * .6)));
      s.style.transform = k < 1 ? 'scale(' + (.93 + .07 * k) + ')' : ''; s.style.borderRadius = k < 1 ? (30 * (1 - k)) + 'px' : '';
    });
  }
  // cards show their titles; hovering (laptops) or tapping (phones) shows the detail line in one panel
  function picker(items, panel, title, body) {
    if (!items.length || !panel) return;
    function pick(it) {
      items.forEach(function (k) { k.classList.toggle('on', k === it); });
      panel.innerHTML = '<b>' + title(it) + '</b>' + body(it);
    }
    items.forEach(function (k) {
      k.setAttribute('tabindex', '0');
      k.addEventListener('click', function () { pick(k); });
      k.addEventListener('mouseenter', function () { pick(k); });
      k.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(k); } });
    });
    pick(items[0]);
  }
  var det2 = document.createElement('p'); det2.className = 'vdetail'; det2.setAttribute('aria-live', 'polite');
  s2.querySelector('.venue-body').appendChild(det2);
  picker([].slice.call(s2.querySelectorAll('.venue-card')), det2,
    function (k) { return k.querySelector('h3').textContent; }, function (k) { return k.querySelector('p').textContent; });
  picker([].slice.call(s3.querySelectorAll('.stop')), s3.querySelector('.jdetail'),
    function (k) { return k.querySelector('.stop-feel').textContent; }, function (k) { return k.querySelector('.stop-behind').textContent; });
  if (reduce) document.documentElement.classList.add('zstatic');
  var ticking = false;
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  layout(); frame();
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', function () { layout(); req(); });
  window.addEventListener('load', function () { layout(); req(); });
  // fonts and images can change heights after load: keep the timeline in step
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { layout(); req(); });
  if (window.ResizeObserver) { var ro = new ResizeObserver(function () { layout(); req(); }); ro.observe(s1); ro.observe(W); }
})();
