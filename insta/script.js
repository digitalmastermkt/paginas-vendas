// ============================================
// Auditoria Instagram @salatielbatistaoficial
// Pequenas interações para o relatório.
// ============================================

(function () {
  'use strict';

  // Smooth scroll para links internos com offset
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (ev) {
      var href = a.getAttribute('href');
      if (!href || href === '#') return;
      var el = document.querySelector(href);
      if (!el) return;
      ev.preventDefault();
      var top = el.getBoundingClientRect().top + window.scrollY - 16;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
  });

  // Animação progressiva do anel de score quando entra na viewport
  var ring = document.querySelector('.ring-fill');
  if (ring) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          ring.style.strokeDashoffset = ring.style.strokeDashoffset || '45.7';
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.4 });
    io.observe(ring);
  }

  // Reveal animado das barras quando entram na viewport
  var bars = document.querySelectorAll('.bar-fill');
  if (bars.length) {
    var io2 = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        var w = el.style.width;
        el.style.width = '0%';
        requestAnimationFrame(function () {
          requestAnimationFrame(function () {
            el.style.width = w;
          });
        });
        io2.unobserve(el);
      });
    }, { threshold: 0.3 });
    bars.forEach(function (b) { io2.observe(b); });
  }

  // Abre o primeiro accordion automaticamente em desktop
  if (window.matchMedia('(min-width: 900px)').matches) {
    var first = document.querySelector('.acc');
    if (first && !first.hasAttribute('open')) first.setAttribute('open', '');
  }
})();
