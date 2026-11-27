(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = document.querySelector('.zworld'), st = W.querySelector('.zstick'),
      z1 = st.querySelector('.z1'), z2 = st.querySelector('.z2'),
      sh = st.querySelector('.zshade--hero'), sw = st.querySelector('.zshade--water'), sc = st.querySelector('.zshade--cabins'),
      cp = W.querySelector('.zcopy'), s2 = W.querySelector('.zs2'), fw = W.querySelector('.zs2 > .wrap'), kids = [].slice.call(W.querySelectorAll('.zs2 > .wrap > *')), s3 = W.querySelector('.zs3');
  var bands = [].slice.call(document.querySelectorAll('.zwin')), secs = [].slice.call(document.querySelectorAll('[data-zoom]'));
  var IW = 1600, IH = 927, FX = .75, FY = .605, ZMID = 3.6, ZEND = 8;   // the cabins' spot in the lagoon photo
  var c = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; }, ease = function (t) { return t * t * (3 - 2 * t); };
  var seg = function (y, a, b) { return ease(c((y - a) / (b - a))); };
  var A = {};
  function layout() {
    var w = st.clientWidth, h = st.clientHeight, s = Math.max(w / IW, h / IH), rw = IW * s, rh = IH * s;
    z1.style.transformOrigin = ((w - rw) * .75 + FX * rw) + 'px ' + ((h - rh) * .5 + FY * rh) + 'px';
    var vh = window.innerHeight, s1 = W.querySelector('.zs1');
    // the framework layer starts at the very top, so it is already pinned while the hero fades
    s2.style.marginTop = (-s1.offsetHeight) + 'px';
    var p3 = parseFloat(getComputedStyle(s3).paddingTop), t2 = s2.offsetTop, h2 = s2.offsetHeight, c3 = s3.offsetTop + p3;
    // zoom and words travel together: both start as you scroll and land at the same moment
    A = { heroOut: vh * .3, z1a: 0, z1b: t2 + vh * .6, fIn0: t2 + vh * .06, fIn1: t2 + vh * .6,
          fOut0: t2 + h2 - vh * 1.45, fOut1: t2 + h2 - vh * 1.1,
          z2a: t2 + h2 - vh * 1.4, z2b: c3 - vh * .55, x0: t2 + h2 - vh * 1.1, x1: c3 - vh * .55 };
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
      var fi = seg(y, A.fIn0, A.fIn1), fo = seg(y, A.fOut0, A.fOut1), fv = fi * (1 - fo);
      sw.style.opacity = seg(y, A.fIn0 - vh * .1, A.fIn1 - vh * .1) * (1 - fo);
      // each block slides in from the left, a beat apart, and all land together as the zoom pauses
      kids.forEach(function (el, i) {
        var a = A.fIn0 + (A.fIn1 - A.fIn0) * i * .12, k = seg(y, a, A.fIn1 - (A.fIn1 - A.fIn0) * (3 - i) * .04), v = k * (1 - fo);
        el.style.opacity = v; el.style.transform = 'translateX(' + (-90 * (1 - k)) + 'px) translateY(' + (-24 * fo) + 'px)';
      });
      fw.style.visibility = (fi * (1 - fo)) < .01 ? 'hidden' : '';
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
  // phones: cards show titles; tapping one shows its description underneath
  var cards = [].slice.call(W.querySelectorAll('.zs2 .venue-card')), det = document.createElement('p');
  det.className = 'vdetail'; det.setAttribute('aria-live', 'polite');
  W.querySelector('.zs2 .venue-body').appendChild(det);
  function pick(card) {
    cards.forEach(function (k) { k.classList.toggle('on', k === card); });
    det.innerHTML = '<b>' + card.querySelector('h3').textContent + '</b>' + card.querySelector('p').textContent;
  }
  cards.forEach(function (k) { k.setAttribute('tabindex', '0'); k.addEventListener('click', function () { pick(k); });
    k.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(k); } }); });
  if (cards.length) pick(cards[0]);
  if (reduce) document.documentElement.classList.add('zstatic');
  var ticking = false;
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  layout(); frame();
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', function () { layout(); req(); });
  window.addEventListener('load', function () { layout(); req(); });
})();
