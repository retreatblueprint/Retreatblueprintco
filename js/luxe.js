// Homepage (luxury redesign): scroll reveals, nav state, hero parallax, client-story pager, voice-note players
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Nav gains a limewash backing once the page moves; hero image drifts a touch slower than the page
  var nav = document.querySelector('nav');
  var heroImg = document.querySelector('.hero-arch .arch img');
  var ticking = false;
  function frame() {
    var y = window.scrollY || 0;
    if (nav) nav.classList.toggle('is-scrolled', y > 24);
    if (heroImg && !reduce && y < 1400) heroImg.style.setProperty('--py', Math.round(y * 0.06) + 'px');
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  frame();

  // Slow fade-up as sections arrive
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Voice notes
  var players = [];
  function fmt(t) { return Math.floor(t / 60) + ':' + ('0' + Math.floor(t % 60)).slice(-2); }
  document.querySelectorAll('.vn').forEach(function (box) {
    var audio = box.querySelector('audio');
    var btn = box.querySelector('button');
    var bar = box.querySelector('.vn-bar');
    var fill = box.querySelector('.vn-fill');
    var time = box.querySelector('.vn-time');
    var total = box.querySelector('.vn-total');
    function pause() { audio.pause(); box.classList.remove('is-playing'); btn.setAttribute('aria-label', 'Play voice note'); }
    players.push(pause);
    btn.addEventListener('click', function () {
      if (audio.paused) {
        players.forEach(function (p) { if (p !== pause) p(); });
        audio.play();
        box.classList.add('is-playing');
        btn.setAttribute('aria-label', 'Pause voice note');
      } else { pause(); }
    });
    audio.addEventListener('loadedmetadata', function () { if (isFinite(audio.duration)) total.textContent = fmt(audio.duration); });
    audio.addEventListener('timeupdate', function () {
      if (isFinite(audio.duration)) fill.style.width = (audio.currentTime / audio.duration * 100) + '%';
      time.textContent = fmt(audio.currentTime);
    });
    audio.addEventListener('ended', function () { pause(); fill.style.width = '0%'; time.textContent = '0:00'; });
    bar.addEventListener('click', function (e) {
      if (!isFinite(audio.duration)) return;
      var r = bar.getBoundingClientRect();
      audio.currentTime = Math.min(Math.max((e.clientX - r.left) / r.width, 0), 1) * audio.duration;
    });
  });

  // Client stories: one at a time, with a pager. The full review opens under the actions row.
  var rc = document.querySelector('.rc');
  if (rc) {
    var stages = Array.prototype.slice.call(rc.querySelectorAll('.stage'));
    var count = rc.querySelector('.pg-count b');
    var cur = 0;
    var show = function (n) {
      cur = (n + stages.length) % stages.length;
      stages.forEach(function (s, k) {
        s.hidden = k !== cur;
        var body = s.querySelector('.rv-body'), btn = s.querySelector('.rv-btn');
        if (body) body.hidden = true;
        if (btn) btn.setAttribute('aria-expanded', 'false');
      });
      count.textContent = ('0' + (cur + 1)).slice(-2);
      players.forEach(function (p) { p(); });
    };
    rc.querySelector('.pg-prev').addEventListener('click', function () { show(cur - 1); });
    rc.querySelector('.pg-next').addEventListener('click', function () { show(cur + 1); });
    rc.querySelectorAll('.rv-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var body = btn.closest('.stage').querySelector('.rv-body');
        var open = body.hidden;
        body.hidden = !open;
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
  }
  // Results: tabbed case studies, each with its own full testimonial
  var cs = document.querySelector('.cs');
  if (cs) {
    var tabs = cs.querySelectorAll('.cs-tab');
    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        tabs.forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
        cs.querySelectorAll('.cs-case').forEach(function (c) {
          var on = c.id === t.getAttribute('aria-controls');
          c.hidden = !on; c.classList.toggle('in', on);
        });
        players.forEach(function (p) { p(); });
      });
    });
    cs.querySelectorAll('.cs-more').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var body = btn.closest('.cs-case').querySelector('.cs-full');
        var open = body.hidden;
        body.hidden = !open;
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
  }
  // Hero reveal: leaves part, then the view settles into the arch window
  var st = document.getElementById('hxStage');
  if (st) {
    var hx = st.querySelector('.hx'), ph = st.querySelector('.hx-ph'), L = st.querySelector('.hx-leaf.l'), Rr = st.querySelector('.hx-leaf.r');
    var cue = st.querySelector('.hx-cue'), copy = st.querySelector('.hero-copy'), arch = st.querySelector('.hero-arch'), archBox = st.querySelector('.hero-arch .arch');
    var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var cl = function (v) { return Math.max(0, Math.min(1, v)); }, ez = function (t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; };
    var wave = function () { var pts = [], n = 24; for (var i = 0; i <= n; i++) pts.push((86 + Math.sin(i * 1.3) * 6 + Math.sin(i * .45) * 5) + '% ' + (i / n * 100) + '%'); return 'polygon(0% 0%, ' + pts.join(', ') + ', 0% 100%)'; };
    L.style.clipPath = Rr.style.clipPath = wave();
    Rr.querySelector('span').style.transform = 'translateY(-50%) scaleX(-1)';
    var hxFrame = function () {
      if (rm) return;
      var V = window.innerHeight, wide = window.innerWidth > 900;
      var span = wide ? st.offsetHeight - V : hx.offsetHeight - V;
      var p = cl(window.scrollY / span);
      var a = ez(cl(p / .42));
      L.style.transform = 'translateX(' + (-a * 105) + '%) scale(' + (1 + a * .2) + ')';
      Rr.style.transform = 'translateX(' + (a * 105) + '%) scale(' + (1 + a * .2) + ') scaleX(-1)';
      cue.style.opacity = 1 - cl(p * 5);
      var b = ez(cl((p - .48) / .4));
      if (wide) {
        var hr = hx.querySelector('.hx-in').getBoundingClientRect(), ar = archBox.getBoundingClientRect();
        var t = (ar.top - hr.top) * b, l = (ar.left - hr.left) * b, r = (hr.right - ar.right) * b, btm = (hr.bottom - ar.bottom) * b, rad = (ar.width / 2) * b;
        ph.style.clipPath = 'inset(' + t + 'px ' + r + 'px ' + btm + 'px ' + l + 'px round ' + rad + 'px ' + rad + 'px 0 0)';
        ph.style.transform = 'scale(' + (1.12 - .12 * a) + ')';
        var done = p > .9;
        hx.style.opacity = done ? 0 : 1;
        arch.style.opacity = done ? 1 : 0;
      } else {
        ph.style.transform = 'scale(' + (1.12 - .12 * a) + ')';
        hx.style.opacity = 1 - b;
        arch.style.opacity = 1;
      }
      copy.style.opacity = cl((p - .55) / .3);
      copy.style.transform = 'translateY(' + (16 - 16 * cl((p - .55) / .3)) + 'px)';
    };
    window.addEventListener('scroll', function () { requestAnimationFrame(hxFrame); }, { passive: true });
    window.addEventListener('resize', hxFrame);
    hxFrame();
  }
  // Roots and journey arc draw in when they come into view
  if ('IntersectionObserver' in window) {
    var dio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('drawn'); dio.unobserve(e.target); } }); }, { threshold: .35 });
    document.querySelectorAll('.venue-soil, .sun').forEach(function (el) { dio.observe(el); });
  } else { document.querySelectorAll('.venue-soil, .sun').forEach(function (el) { el.classList.add('drawn'); }); }
})();
