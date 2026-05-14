// Dossiê varaldomanto — animações leves de entrada e progressive enhancement.
(function () {
  'use strict';

  // Anima as barras BMAD + mix de formato + score ring quando entram em viewport.
  const animatables = document.querySelectorAll('.bar-fill, .mix-fill, .ring-fill');

  if (!('IntersectionObserver' in window)) {
    // Fallback: já mostra direto sem animar.
    return;
  }

  // Captura valor inicial e zera (pra animar).
  animatables.forEach(el => {
    if (el.classList.contains('ring-fill')) {
      const initial = el.style.strokeDashoffset;
      el.dataset.target = initial;
      el.style.strokeDashoffset = '326.7'; // ring zerado
    } else {
      const w = el.style.width;
      el.dataset.target = w;
      el.style.width = '0';
    }
  });

  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = el.dataset.target;
      if (el.classList.contains('ring-fill')) {
        el.style.strokeDashoffset = target;
      } else {
        el.style.width = target;
      }
      obs.unobserve(el);
    });
  }, { threshold: 0.3, rootMargin: '0px 0px -10% 0px' });

  animatables.forEach(el => obs.observe(el));

  // Fade-in suave dos blocos.
  const blocks = document.querySelectorAll('.block, .hero-inner > *');
  const fadeObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        fadeObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  blocks.forEach(b => fadeObs.observe(b));
})();
