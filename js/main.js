const canHoverTestimonials = window.matchMedia('(hover: hover)').matches;

function setActiveTestimonial(who) {
  ['cris', 'jon'].forEach(function (id) {
    const card = document.getElementById('card-' + id);
    const reviewOpen = card.querySelector('details[open]') !== null;
    // A card whose full review is open stays open until "Collapse review" is pressed
    card.classList.toggle('is-active', who === id || reviewOpen);
  });
}

function handleTestimonialHover(who) {
  if (!canHoverTestimonials || Date.now() < ignoreHoverUntil) return;
  pinnedTestimonial = null;
  setActiveTestimonial(who);
}

// Set when a visitor jumps here from "Hear ... voice note", so the card stays open
let pinnedTestimonial = null;
let ignoreHoverUntil = 0; // cards slide under a still mouse while the page scrolls to them

function resetTestimonials() {
  if (!canHoverTestimonials || Date.now() < ignoreHoverUntil) return;
  setActiveTestimonial(pinnedTestimonial);
}

function handleTestimonialTap(who) {
  if (canHoverTestimonials) return;
  const card = document.getElementById('card-' + who);
  const isActive = card.classList.contains('is-active');
  setActiveTestimonial(isActive ? null : who);
}

const audio = document.getElementById('testimonialAudio');
const playBtn = document.getElementById('playBtn');
const playIcon = document.getElementById('playIcon');
const pauseIcon = document.getElementById('pauseIcon');
const progressFill = document.getElementById('progressFill');
const timeDisplay = document.getElementById('timeDisplay');

function togglePlay() {
  if (audio.paused) {
    audio.play();
    playIcon.style.display = 'none';
    pauseIcon.style.display = 'block';
    playBtn.style.background = '#3a5a3e';
  } else {
    audio.pause();
    playIcon.style.display = 'block';
    pauseIcon.style.display = 'none';
    playBtn.style.background = 'var(--sage-dark)';
  }
}

audio.addEventListener('timeupdate', function() {
  const pct = (audio.currentTime / audio.duration) * 100;
  progressFill.style.width = pct + '%';
  const mins = Math.floor(audio.currentTime / 60);
  const secs = Math.floor(audio.currentTime % 60).toString().padStart(2, '0');
  timeDisplay.textContent = mins + ':' + secs;
});

audio.addEventListener('ended', function() {
  playIcon.style.display = 'block';
  pauseIcon.style.display = 'none';
  playBtn.style.background = 'var(--sage-dark)';
  progressFill.style.width = '0%';
  timeDisplay.textContent = '0:00';
});

function seekAudio(e) {
  if (!isFinite(audio.duration)) return;
  const bar = document.getElementById('progressBar');
  const rect = bar.getBoundingClientRect();
  const pct = (e.clientX - rect.left) / rect.width;
  audio.currentTime = pct * audio.duration;
}

const audio2 = document.getElementById('testimonialAudio2');
const playBtn2 = document.getElementById('playBtn2');
const playIcon2 = document.getElementById('playIcon2');
const pauseIcon2 = document.getElementById('pauseIcon2');
const progressFill2 = document.getElementById('progressFill2');
const timeDisplay2 = document.getElementById('timeDisplay2');

function togglePlay2() {
  if (audio2.paused) {
    audio2.play();
    playIcon2.style.display = 'none';
    pauseIcon2.style.display = 'block';
    playBtn2.style.background = '#3a5a3e';
  } else {
    audio2.pause();
    playIcon2.style.display = 'block';
    pauseIcon2.style.display = 'none';
    playBtn2.style.background = 'var(--sage-dark)';
  }
}

audio2.addEventListener('timeupdate', function() {
  const pct = (audio2.currentTime / audio2.duration) * 100;
  progressFill2.style.width = pct + '%';
  const mins = Math.floor(audio2.currentTime / 60);
  const secs = Math.floor(audio2.currentTime % 60).toString().padStart(2, '0');
  timeDisplay2.textContent = mins + ':' + secs;
});

audio2.addEventListener('ended', function() {
  playIcon2.style.display = 'block';
  pauseIcon2.style.display = 'none';
  playBtn2.style.background = 'var(--sage-dark)';
  progressFill2.style.width = '0%';
  timeDisplay2.textContent = '0:00';
});

function seekAudio2(e) {
  if (!isFinite(audio2.duration)) return;
  const bar = document.getElementById('progressBar2');
  const rect = bar.getBoundingClientRect();
  const pct = (e.clientX - rect.left) / rect.width;
  audio2.currentTime = pct * audio2.duration;
}

// Close an open full review from the button at its bottom, then bring the card back into view
function collapseReview(btn) {
  const details = btn.closest('details');
  const card = details.closest('.testimonial-card');
  details.open = false;
  details.querySelector('summary').focus({ preventScroll: true });
  const r = card.getBoundingClientRect();
  if (r.top < 90 || r.bottom > window.innerHeight) {
    card.scrollIntoView({ block: 'center', behavior: 'smooth' });
  }
}

// Touch devices have no hover, so say "Tap" instead
if (!canHoverTestimonials) {
  document.querySelectorAll('.testimonial-hint span').forEach(function (el) {
    el.textContent = 'Tap to listen';
  });
}


// In practice: tabbed case studies, each linked to its client's testimonial below
const practiceCases = [
  { who: 'cris', label: "Hear Cris's voice note" },
  { who: 'jon', label: "Hear Jonathon's voice note" }
];
let practiceIndex = 0;

function showPractice(i) {
  practiceIndex = (i + practiceCases.length) % practiceCases.length;
  practiceCases.forEach(function (_, n) {
    const on = n === practiceIndex;
    const tab = document.getElementById('ptab-' + n);
    const panel = document.getElementById('ppanel-' + n);
    tab.classList.toggle('is-active', on);
    tab.setAttribute('aria-selected', on ? 'true' : 'false');
    panel.classList.toggle('is-active', on);
    panel.hidden = !on;
  });
  document.querySelectorAll('.practice-dots span').forEach(function (d, n) {
    d.classList.toggle('is-active', n === practiceIndex);
  });
  const c = practiceCases[practiceIndex];
  document.getElementById('practiceVoiceText').textContent = c.label;
  document.getElementById('practiceVoice').setAttribute('href', '#card-' + c.who);
}

function stepPractice(dir) { showPractice(practiceIndex + dir); }

function goToTestimonial(e) {
  e.preventDefault();
  const who = practiceCases[practiceIndex].who;
  const card = document.getElementById('card-' + who);
  card.scrollIntoView({ behavior: 'smooth', block: 'center' });
  pinnedTestimonial = who;
  ignoreHoverUntil = Date.now() + 1500;
  setActiveTestimonial(who);
  card.classList.add('is-spotlit');
  setTimeout(function () { card.classList.remove('is-spotlit'); }, 2400);
}
