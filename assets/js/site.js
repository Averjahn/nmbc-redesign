/* НМБК редизайн — общий скрипт: версия для слабовидящих, мобильное меню, слайдер */
(function () {
  // ---- Версия для слабовидящих (с сохранением) ----
  var KEY = 'nmbc-a11y';
  function applyA11y(on) {
    document.body.classList.toggle('a11y', on);
    var btn = document.getElementById('a11yBtn');
    if (btn) btn.setAttribute('aria-pressed', on ? 'true' : 'false');
  }
  try { if (localStorage.getItem(KEY) === '1') applyA11y(true); } catch (e) {}
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('#a11yBtn');
    if (!btn) return;
    var on = !document.body.classList.contains('a11y');
    applyA11y(on);
    try { localStorage.setItem(KEY, on ? '1' : '0'); } catch (e) {}
  });

  // ---- Мобильное меню ----
  var mobileNav = document.getElementById('mobileNav');
  function openNav() { if (mobileNav) { mobileNav.classList.add('open'); document.body.style.overflow = 'hidden'; } }
  function closeNav() { if (mobileNav) { mobileNav.classList.remove('open'); document.body.style.overflow = ''; } }
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('#burger')) return openNav();
    if (e.target.closest && e.target.closest('#mnClose')) return closeNav();
    if (e.target === mobileNav) return closeNav();
    var acc = e.target.closest && e.target.closest('.mn-acc > button');
    if (acc && acc.parentElement.querySelector('.mn-sub')) { acc.parentElement.classList.toggle('open'); }
    if (e.target.closest && e.target.closest('.mn-sub a, .mn-cta')) closeNav();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

  // ---- Слайдер на главной ----
  var slides = document.querySelectorAll('.hero-media .slide');
  if (slides.length > 1) {
    var i = 0;
    setInterval(function () {
      slides[i].classList.remove('on');
      i = (i + 1) % slides.length;
      slides[i].classList.add('on');
    }, 4000);
  }
})();
