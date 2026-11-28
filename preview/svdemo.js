/* Service-page demo boards: a sample venue's week (Concierge Ops) or half-year (Director) that plays on a loop.
   Numbers are illustrative and labelled as such on the board. Plays only while the board is on screen. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(r, s) { return r.querySelector(s); }
  function $$(r, s) { return [].slice.call(r.querySelectorAll(s)); }
  function fmt(n) { return n.toLocaleString('en-US'); }
  function onScreen(el, cb) {
    if (!('IntersectionObserver' in window)) { cb(true); return; }
    new IntersectionObserver(function (es) { es.forEach(function (e) { cb(e.isIntersecting); }); }, { threshold: .25 }).observe(el);
  }
  function logLine(list, html, max) {
    var li = document.createElement('li'); li.innerHTML = html; li.className = 'dm-new';
    list.insertBefore(li, list.firstChild);
    requestAnimationFrame(function () { requestAnimationFrame(function () { li.className = ''; }); });
    while (list.children.length > max) list.removeChild(list.lastChild);
  }

  /* ---------- Concierge Ops: one week of the inbox ---------- */
  var DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  var CEV = [ // [hour of week, source, lang, role, text, flagged]
    [1.2, 0, 'EN', 0, 'Inquiry for a 5-night yoga retreat · replied in your voice', 0],
    [3.5, 1, 'ES', 1, 'Guest asks about airport pickup · answered, details sent', 0],
    [6.0, 2, 'EN', 0, 'Booking.com request · calendar updated, confirmation sent', 0],
    [9.4, 0, 'EN', 0, 'Group of 14 asks for a custom rate · flagged for your pricing call', 1],
    [13.1, 3, 'ES', 2, 'Retreat leader sends rooming changes · list updated', 0],
    [17.8, 0, 'EN', 0, 'Interested guest went quiet · day-2 follow-up sent', 0],
    [22.0, 1, 'EN', 1, 'Pre-arrival form and dietary intake sent to 9 guests', 0],
    [27.5, 0, 'EN', 3, 'Deposit received · invoice marked paid', 0],
    [31.0, 0, 'ES', 0, 'Inquiry for a couples retreat · replied in Spanish', 0],
    [36.2, 1, 'EN', 1, 'Reminders sent for Friday arrivals', 0],
    [41.5, 2, 'EN', 0, 'Airbnb message about late check-in · answered', 0],
    [45.0, 0, 'EN', 0, 'Request for a private chef night · flagged as a special request', 1],
    [50.3, 3, 'EN', 2, 'Schedule and meal plan ready for next week&rsquo;s group', 0],
    [55.8, 1, 'EN', 1, 'Review requests sent after Sunday checkout', 0],
    [60.4, 0, 'EN', 3, 'Month-end summary drafted: what came in, what&rsquo;s owed', 0]
  ];
  function concierge(b) {
    var T = 64, t = 0, i = 0, last = 0, playing = false, raf;
    var clock = $(b, '.dm-clock'), knob = $(b, '.dm-knob'), list = $(b, '.dm-log ul');
    var k = $$(b, '.dm-kpi b'), src = $$(b, '.dm-src'), roles = $$(b, '.dm-role'), q = $(b, '.dm-q');
    var rc = [0, 0, 0, 0], flagged = 0;
    function reset() { t = 0; i = 0; rc = [0, 0, 0, 0]; flagged = 0; list.innerHTML = ''; q.innerHTML = '';
      roles.forEach(function (r) { $(r, 'i').textContent = '0'; }); }
    function draw() {
      var p = t / T, hw = p * 168, d = Math.min(6, Math.floor(hw / 24)), hh = Math.floor(hw % 24), mm = Math.floor((hw * 60) % 60);
      clock.textContent = DAYS[d] + ' ' + (hh < 10 ? '0' : '') + hh + ':' + (mm < 10 ? '0' : '') + mm;
      knob.style.left = (p * 100) + '%';
      k[0].textContent = fmt(Math.round(214 * p));
      k[1].textContent = (34 + Math.round(10 * Math.abs(Math.sin(t / 5)))) + ' min';
      k[2].textContent = flagged;
      k[3].textContent = Math.round(19 * p) + ' h';
    }
    function fire(e) {
      var s = src[e[1]], r = roles[e[3]];
      s.classList.add('on'); r.classList.add('on');
      setTimeout(function () { s.classList.remove('on'); r.classList.remove('on'); }, 900);
      rc[e[3]]++; $(r, 'i').textContent = rc[e[3]];
      if (e[5]) { flagged++; var c = document.createElement('span'); c.textContent = ['Pricing', 'Special request'][flagged % 2 ? 0 : 1]; q.appendChild(c); }
      var hw = e[0] / 64 * 168, d = Math.floor(hw / 24), hh = Math.floor(hw % 24);
      logLine(list, '<time>' + DAYS[d] + ' ' + (hh < 10 ? '0' : '') + hh + ':00</time><em class="dm-lang">' + e[2] + '</em>' + e[4] + (e[5] ? ' <strong>for you</strong>' : ''), 4);
    }
    function step(now) {
      if (!playing) return;
      var dt = last ? Math.min(.1, (now - last) / 1000) : 0; last = now; t += dt;
      while (i < CEV.length && CEV[i][0] <= t) fire(CEV[i++]);
      if (t >= T) { reset(); }
      draw(); raf = requestAnimationFrame(step);
    }
    if (reduce) { t = T * .97; CEV.forEach(fire); draw(); return; }
    draw();
    onScreen(b, function (vis) { playing = vis; last = 0; cancelAnimationFrame(raf); if (vis) raf = requestAnimationFrame(step); });
  }

  /* ---------- Director: six months of numbers ---------- */
  var M = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  var D = { occ: [48, 50, 54, 57, 60, 63], be: [52, 52, 50, 49, 48, 48], adr: [138, 138, 142, 146, 149, 152], cpor: [71, 72, 69, 65, 64, 63], cash: [-4.2, -2.6, -0.4, 1.8, 3.1, 4.6] };
  var DEV = [ // [month position 0..6, text]
    [0.15, 'Monthly owner report set up from your booking and payment records'],
    [0.7, 'Break-even occupancy calculated for the first time'],
    [1.3, 'Booking-mix review: midweek retreats priced below cost'],
    [2.1, 'Midweek package repriced against cost per occupied room'],
    [2.8, 'Linen and laundry re-quoted with two vendors'],
    [3.5, 'Budget versus actuals reviewed with the owner'],
    [4.3, 'Shoulder-season cash plan agreed'],
    [5.1, 'High-season forecast: staffing set to confirmed bookings']
  ];
  function lerp(a, p) { var x = Math.min(a.length - 1, p), i0 = Math.floor(x), i1 = Math.min(a.length - 1, i0 + 1), f = x - i0; return a[i0] + (a[i1] - a[i0]) * f; }
  function director(b) {
    var T = 42, t = 0, i = 0, last = 0, playing = false, raf;
    var clock = $(b, '.dm-clock'), knob = $(b, '.dm-knob'), list = $(b, '.dm-log ul'), k = $$(b, '.dm-kpi b');
    var occ = $(b, '.dm-occ'), be = $(b, '.dm-be'), dot = $(b, '.dm-dot');
    var W = 600, H = 200, x = function (m) { return 20 + m * (W - 40) / 5; }, y = function (v) { return H - 20 - (v - 40) * (H - 40) / 30; };
    function path(a, p) { var s = ''; for (var m = 0; m <= Math.min(5, p); m += .05) s += (s ? 'L' : 'M') + x(m).toFixed(1) + ' ' + y(lerp(a, m)).toFixed(1); return s; }
    function draw() {
      var p = Math.min(5, t / T * 6);
      clock.textContent = M[Math.min(5, Math.floor(t / T * 6))] + ' report';
      knob.style.left = (p / 5 * 100) + '%';
      var o = lerp(D.occ, p), adr = lerp(D.adr, p), c = lerp(D.cash, p);
      k[0].textContent = Math.round(o) + '%';
      k[1].textContent = '$' + Math.round(adr);
      k[2].textContent = '$' + Math.round(adr * o / 100);
      k[3].textContent = '$' + Math.round(lerp(D.cpor, p));
      k[4].textContent = Math.round(lerp(D.be, p)) + '%';
      k[5].textContent = (c < 0 ? '−$' : '+$') + Math.abs(c).toFixed(1) + 'k';
      k[5].parentNode.classList.toggle('neg', c < 0);
      occ.setAttribute('d', path(D.occ, p)); be.setAttribute('d', path(D.be, 5));
      dot.setAttribute('cx', x(p)); dot.setAttribute('cy', y(o));
    }
    function step(now) {
      if (!playing) return;
      var dt = last ? Math.min(.1, (now - last) / 1000) : 0; last = now; t += dt;
      var p = t / T * 6;
      while (i < DEV.length && DEV[i][0] <= p) { logLine(list, '<time>' + M[Math.min(5, Math.floor(DEV[i][0]))] + '</time>' + DEV[i][1], 4); i++; }
      if (t >= T + 3) { t = 0; i = 0; list.innerHTML = ''; }
      draw(); raf = requestAnimationFrame(step);
    }
    if (reduce) { t = T; DEV.slice(-4).forEach(function (e) { logLine(list, '<time>' + M[Math.floor(e[0])] + '</time>' + e[1], 4); }); draw(); return; }
    draw();
    onScreen(b, function (vis) { playing = vis; last = 0; cancelAnimationFrame(raf); if (vis) raf = requestAnimationFrame(step); });
  }

  $$(document, '.dm[data-demo="concierge"]').forEach(concierge);
  $$(document, '.dm[data-demo="director"]').forEach(director);
})();
