/* НМБК редизайн — общий скрипт: панель «Версия для слабовидящих», меню, слайдер, таблицы */
(function () {
  var B = document.body, KEY = 'nmbc-av';
  var state = { on: false, font: '2', scheme: 'default', img: 'on' };
  try { var saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if (saved) state = Object.assign(state, saved); } catch (e) {}

  function press(sel, attr, val) {
    document.querySelectorAll(sel).forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute(attr) === val ? 'true' : 'false');
    });
  }
  function applyAV() {
    B.classList.toggle('av', state.on);
    B.setAttribute('data-font', state.on ? state.font : '1');
    B.setAttribute('data-scheme', state.on ? state.scheme : 'default');
    B.classList.toggle('av-noimg', state.on && state.img === 'off');
    var btn = document.getElementById('a11yBtn');
    if (btn) btn.setAttribute('aria-pressed', state.on ? 'true' : 'false');
    press('[data-av-font]', 'data-av-font', state.font);
    press('[data-av-scheme]', 'data-av-scheme', state.scheme);
    press('[data-av-img]', 'data-av-img', state.img);
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
  }
  applyAV();

  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target : e.target.parentElement;
    // тумблер версии
    if (e.target.closest && e.target.closest('#a11yBtn')) { state.on = !state.on; return applyAV(); }
    if (e.target.closest && e.target.closest('#avOff')) { state.on = false; return applyAV(); }
    var fb = e.target.closest && e.target.closest('[data-av-font]');
    if (fb) { state.on = true; state.font = fb.getAttribute('data-av-font'); return applyAV(); }
    var sb = e.target.closest && e.target.closest('[data-av-scheme]');
    if (sb) { state.on = true; state.scheme = sb.getAttribute('data-av-scheme'); return applyAV(); }
    var ib = e.target.closest && e.target.closest('[data-av-img]');
    if (ib) { state.on = true; state.img = ib.getAttribute('data-av-img'); return applyAV(); }

    // мобильное меню
    if (e.target.closest && e.target.closest('#burger')) return openNav();
    if (e.target.closest && e.target.closest('#mnClose')) return closeNav();
    if (e.target === mobileNav) return closeNav();
    var acc = e.target.closest && e.target.closest('.mn-acc > button');
    if (acc && acc.parentElement.querySelector('.mn-sub')) acc.parentElement.classList.toggle('open');
    if (e.target.closest && e.target.closest('.mn-sub a, .mn-cta')) closeNav();
  });

  // ---- Мобильное меню ----
  var mobileNav = document.getElementById('mobileNav');
  function openNav() { if (mobileNav) { mobileNav.classList.add('open'); B.style.overflow = 'hidden'; } }
  function closeNav() { if (mobileNav) { mobileNav.classList.remove('open'); B.style.overflow = ''; } }
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

  // ---- Таблицы в контенте: горизонтальная прокрутка на узких экранах ----
  document.querySelectorAll('.prose table').forEach(function (tb) {
    if (tb.parentElement && tb.parentElement.classList.contains('table-scroll')) return;
    var w = document.createElement('div');
    w.className = 'table-scroll';
    tb.parentNode.insertBefore(w, tb);
    w.appendChild(tb);
  });
})();
