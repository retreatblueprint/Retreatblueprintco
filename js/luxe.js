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
})();
