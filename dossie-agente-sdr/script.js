
(function() {
  var menuBtn = document.getElementById('menuToggle');
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('overlay');
  var backTop = document.getElementById('backTop');

  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
    menuBtn.classList.remove('active');
    document.body.style.overflow = '';
  }
  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('active');
    menuBtn.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  menuBtn.addEventListener('click', function() {
    if (sidebar.classList.contains('open')) closeSidebar();
    else openSidebar();
  });
  overlay.addEventListener('click', closeSidebar);

  // Fecha menu ao clicar em link no mobile
  document.querySelectorAll('.sidebar-link').forEach(function(a) {
    a.addEventListener('click', function() {
      if (window.innerWidth <= 768) closeSidebar();
    });
  });

  // Active link tracking via IntersectionObserver
  var sections = document.querySelectorAll('section.block');
  var links = {};
  document.querySelectorAll('.sidebar-link').forEach(function(a) {
    var href = a.getAttribute('href');
    if (href && href.charAt(0) === '#') links[href.slice(1)] = a;
  });

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        var id = entry.target.id;
        var link = links[id];
        if (!link) return;
        if (entry.isIntersecting) {
          Object.keys(links).forEach(function(k) { links[k].classList.remove('active'); });
          link.classList.add('active');
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });
    sections.forEach(function(s) { observer.observe(s); });
  }

  // Back to top
  window.addEventListener('scroll', function() {
    if (window.scrollY > 600) backTop.classList.add('visible');
    else backTop.classList.remove('visible');
  }, { passive: true });
  backTop.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Esc fecha sidebar
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && sidebar.classList.contains('open')) closeSidebar();
  });
})();
