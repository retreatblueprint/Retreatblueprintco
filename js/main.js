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
  if (canHoverTestimonials) setActiveTestimonial(who);
}

function resetTestimonials() {
  if (canHoverTestimonials) setActiveTestimonial(null);
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
