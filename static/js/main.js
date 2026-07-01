/* ============================================================
   AI Research Paper Discovery Engine — main.js
   ============================================================ */

'use strict';

// ── Sticky Navbar ──────────────────────────────────────────
(function () {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;
  const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 20);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

// ── Auto-resize textarea ───────────────────────────────────
(function () {
  const ta = document.getElementById('questionInput');
  if (!ta) return;
  const resize = () => {
    ta.style.height = 'auto';
    ta.style.height = Math.min(ta.scrollHeight, 160) + 'px';
  };
  ta.addEventListener('input', resize);
  resize();
})();

// ── Send on Enter (Shift+Enter = newline) ─────────────────
(function () {
  const ta   = document.getElementById('questionInput');
  const form = document.getElementById('chatForm');
  if (!ta || !form) return;
  ta.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      form.requestSubmit ? form.requestSubmit() : form.submit();
    }
  });
})();

// ── Chat: auto-scroll to bottom ───────────────────────────
(function () {
  const chat = document.getElementById('chatArea');
  if (!chat) return;
  const scrollBottom = () => { chat.scrollTop = chat.scrollHeight; };
  scrollBottom();
  const observer = new MutationObserver(scrollBottom);
  observer.observe(chat, { childList: true, subtree: true });
})();

// ── Copy answer to clipboard ──────────────────────────────
document.addEventListener('click', function (e) {
  const btn = e.target.closest('[data-copy]');
  if (!btn) return;
  const text = btn.getAttribute('data-copy');
  navigator.clipboard.writeText(text).then(() => {
    const original = btn.innerHTML;
    btn.innerHTML = '<i class="bi bi-check2"></i> Copied';
    setTimeout(() => { btn.innerHTML = original; }, 1800);
  });
});

// ── Quick-prompt chips → textarea ─────────────────────────
document.addEventListener('click', function (e) {
  const chip = e.target.closest('.quick-prompt-btn');
  if (!chip) return;
  const ta = document.getElementById('questionInput');
  if (!ta) return;
  ta.value = chip.textContent.trim();
  ta.focus();
  ta.dispatchEvent(new Event('input'));
});

// ── Hint chips on hero → search input ─────────────────────
document.addEventListener('click', function (e) {
  const chip = e.target.closest('.hint-chip');
  if (!chip) return;
  const input = document.getElementById('heroSearchInput');
  if (!input) return;
  input.value = chip.textContent.trim();
  input.focus();
});

// ── Staggered card animation on scroll ────────────────────
(function () {
  if (!('IntersectionObserver' in window)) return;
  const cards = document.querySelectorAll('.feature-card, .paper-card');
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        entry.target.style.animationDelay = (i * 0.06) + 's';
        entry.target.classList.add('animate-fade-up');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  cards.forEach(c => io.observe(c));
})();

// ── Flash message auto-dismiss ────────────────────────────
(function () {
  document.querySelectorAll('.alert-dismissible').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });
})();
