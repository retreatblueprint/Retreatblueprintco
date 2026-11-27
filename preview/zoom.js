(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) { document.documentElement.classList.add('zstatic'); return; }
  var sc = document.querySelector('.zscene'), st = sc.querySelector('.zstick'),
      z1 = sc.querySelector('.z1'), z2 = sc.querySelector('.z2'),
      cp = sc.querySelector('.zcopy'), sh = sc.querySelector('.zshade');
  var IW = 1600, IH = 927, FX = .75, FY = .605;   // where the cabins sit in the lagoon photo
  var bands = [].slice.call(document.querySelectorAll('.zwin'));
  var secs = [].slice.call(document.querySelectorAll('[data-zoom]'));
  var c = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var ease = function (t) { return t * t * (3 - 2 * t); };
  function origin() {   // keep the zoom aimed at the cabins at any screen shape
    var w = st.clientWidth, h = st.clientHeight, s = Math.max(w / IW, h / IH), rw = IW * s, rh = IH * s;
    z1.style.transformOrigin = ((w - rw) * .75 + FX * rw) + 'px ' + ((h - rh) * .5 + FY * rh) + 'px';
  }
  function frame() {
    ticking = false;
    var vh = window.innerHeight, r = sc.getBoundingClientRect(), range = sc.offsetHeight - vh;
    if (r.bottom > -vh) {
      var p = c(-r.top / range), zp = ease(c(p / .7));
      z1.style.transform = 'scale(' + (1 + zp * 6.5) + ')';
      var f = ease(c((p - .42) / .26));
      z2.style.opacity = f; z2.style.transform = 'scale(' + (1.35 - .35 * f) + ')';
      var t = c(p / .2);
      cp.style.opacity = 1 - t; cp.style.transform = 'translateY(' + (-60 * t) + 'px)';
      cp.style.pointerEvents = t > .6 ? 'none' : '';
      sh.style.opacity = 1 - t;
    }
    bands.forEach(function (b) {
      var q = b.getBoundingClientRect(); if (q.bottom < 0 || q.top > vh) return;
      var k = ease(c((vh - q.top) / (vh * .85)));
      b.style.setProperty('--ix', (18 * (1 - k)) + '%'); b.style.setProperty('--iy', (10 * (1 - k)) + '%');
      b.style.setProperty('--rr', (28 * (1 - k)) + 'px'); b.style.setProperty('--zs', 1.25 - .25 * k);
    });
    secs.forEach(function (s) {
      var q = s.getBoundingClientRect(); if (q.top > vh || q.bottom < 0) return;
      var k = ease(c((vh - q.top) / (vh * .6)));
      s.style.transform = k < 1 ? 'scale(' + (.93 + .07 * k) + ')' : '';
      s.style.borderRadius = k < 1 ? (30 * (1 - k)) + 'px' : '';
    });
  }
  var ticking = false;
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  origin(); frame();
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', function () { origin(); req(); });
})();
