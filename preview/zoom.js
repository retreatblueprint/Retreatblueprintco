(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = document.querySelector('.zworld'), st = W.querySelector('.zstick'),
      z1 = st.querySelector('.z1'), z2 = st.querySelector('.z2'),
      sh = st.querySelector('.zshade--hero'), sw = st.querySelector('.zshade--water'), sc = st.querySelector('.zshade--cabins'),
      cp = W.querySelector('.zcopy'), s2 = W.querySelector('.zs2'), s3 = W.querySelector('.zs3');
  var bands = [].slice.call(document.querySelectorAll('.zwin')), secs = [].slice.call(document.querySelectorAll('[data-zoom]'));
  var IW = 1600, IH = 927, FX = .75, FY = .605, ZMID = 3.6, ZEND = 8;   // the cabins' spot in the lagoon photo
  var c = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; }, ease = function (t) { return t * t * (3 - 2 * t); };
  var seg = function (y, a, b) { return ease(c((y - a) / (b - a))); };
  var A = {};
  function layout() {
    var w = st.clientWidth, h = st.clientHeight, s = Math.max(w / IW, h / IH), rw = IW * s, rh = IH * s;
    z1.style.transformOrigin = ((w - rw) * .75 + FX * rw) + 'px ' + ((h - rh) * .5 + FY * rh) + 'px';
    var vh = window.innerHeight, p2 = parseFloat(getComputedStyle(s2).paddingTop), p3 = parseFloat(getComputedStyle(s3).paddingTop);
    var c2 = s2.offsetTop + p2, c3 = s3.offsetTop + p3, e2 = s2.offsetTop + s2.offsetHeight - parseFloat(getComputedStyle(s2).paddingBottom);
    A = { heroOut: vh * .45, z1a: 0, z1b: c2 - vh * .6, wIn0: c2 - vh * .95, wIn1: c2 - vh * .6,
          z2a: e2 - vh * .55, z2b: c3 - vh * .55, x0: e2 - vh * .2, x1: c3 - vh * .55 };
  }
  function frame() {
    ticking = false;
    var vh = window.innerHeight, y = -W.getBoundingClientRect().top;
    if (y < W.offsetHeight) {
      var h = c(y / A.heroOut);
      cp.style.opacity = 1 - h; cp.style.transform = 'translateY(' + (-70 * h) + 'px)'; sh.style.opacity = 1 - h;
      if (!reduce) {
        var k1 = seg(y, A.z1a, A.z1b), k2 = seg(y, A.z2a, A.z2b);
        z1.style.transform = 'scale(' + (1 + (ZMID - 1) * k1 + (ZEND - ZMID) * k2) + ')';
      }
      var x = seg(y, A.x0, A.x1);
      z2.style.opacity = x; if (!reduce) z2.style.transform = 'scale(' + (1.35 - .35 * x) + ')';
      sw.style.opacity = seg(y, A.wIn0, A.wIn1) * (1 - seg(y, A.z2a, A.x0 + vh * .15));
      sc.style.opacity = x;
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
  if (reduce) document.documentElement.classList.add('zstatic');
  var ticking = false;
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  layout(); frame();
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', function () { layout(); req(); });
  window.addEventListener('load', function () { layout(); req(); });
})();
