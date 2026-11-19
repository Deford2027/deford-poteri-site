/* Город посетителя. Спрос снят по городам из DATA.regions; выбор запоминается и общий для всех страниц.
   По умолчанию – Минск. Автоопределение по IP в статике не делаем (в прототипе оно шло через сторонний сервис;
   на бою – только своим сервером). Кнопки города – любой .js-city-btn. Подписка: CITY.onChange(fn). */
(function () {
  var D = window.DATA, KEY = 'poteri-city', subs = [];
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var saved = store.get(KEY), cur = saved && D.regions[saved] ? saved : (D.defaultRegion || 'mnsk');
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var niches = D.niches.map(function (n) { return '<option>' + esc(n.name) + '</option>'; }).join('') + '<option>Другое</option>';

  var back = document.createElement('div');
  back.className = 'c-back';
  back.innerHTML = '<div class="c-win" role="dialog" aria-modal="true" aria-labelledby="c-title">' +
    '<button class="c-x" type="button" aria-label="Закрыть">×</button>' +
    '<h3 id="c-title">В каком городе ваш бизнес?</h3>' +
    '<p class="muted c-intro">Покажем, сколько клиентов ищут ваши услуги и сколько уходит мимо – именно в вашем городе.</p>' +
    '<div class="c-list">' + Object.keys(D.regions).map(function (r) {
      return '<button class="btn btn--ghost" type="button" data-city="' + r + '">' + esc(D.regions[r]) + '</button>';
    }).join('') + '<button class="btn btn--ghost c-wide" type="button" data-city="other">Другой город<span aria-hidden="true">→</span></button></div>' +
    '<form class="form c-other js-form">' +
      '<p><b>По вашему городу снимем спрос отдельно.</b> Оставьте заявку – пришлём расчёт потерь по вашей нише.</p>' +
      '<label class="field">Город<input class="input" name="city" autocomplete="address-level2" required></label>' +
      '<label class="field">Ниша<select class="select" name="niche">' + niches + '</select></label>' +
      '<label class="field">Телефон<input class="input" name="phone" type="tel" inputmode="tel" placeholder="+375 (__) ___-__-__" required></label>' +
      '<label class="check"><input class="cbox" type="checkbox" data-agree> <span>Согласен на обработку <a href="#">персональных данных</a></span></label>' +
      '<button class="btn btn--block" type="submit" disabled>Снять спрос по моему городу</button>' +
      '<p class="form__hint">Снимем спрос по вашему городу и нише и пришлём расчёт в Telegram или Макс</p>' +
      '<button class="btn btn--ghost btn--block" type="button" data-back>← Назад к городам</button>' +
      '<div class="form__ok"><div class="form__ok-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>' +
        '<h3>Заявка принята</h3><p class="muted">Снимем спрос по вашему городу и пришлём расчёт в Telegram или Макс.</p>' +
        '<p class="muted">Срочно – <a href="tel:+79537777891">позвонить</a> или <a href="https://t.me/Artem1Galimov" target="_blank" rel="noopener">написать в Telegram</a>.</p></div>' +
    '</form></div>';
  document.body.appendChild(back);
  var win = back.querySelector('.c-win'), form = back.querySelector('form'), lastFocus = null;

  function paint() {
    document.querySelectorAll('.js-city-btn').forEach(function (b) { b.innerHTML = esc(D.regions[cur]) + ' <span aria-hidden="true">▾</span>'; });
    back.querySelectorAll('[data-city]').forEach(function (b) { b.classList.toggle('on', b.dataset.city === cur); });
  }
  function set(r) { cur = r; store.set(KEY, r); paint(); subs.forEach(function (fn) { fn(cur); }); }
  function open() {
    lastFocus = document.activeElement; win.classList.remove('other'); form.classList.remove('sent');
    back.classList.add('open'); back.querySelector('.c-x').focus();
  }
  function close() { back.classList.remove('open'); if (lastFocus && lastFocus.focus) lastFocus.focus(); }
  back.addEventListener('click', function (e) {
    var t = e.target.closest('[data-city],[data-back],.c-x');
    if (e.target === back || (t && t.classList.contains('c-x'))) return close();
    if (!t) return;
    if (t.hasAttribute('data-back')) return win.classList.remove('other');
    if (t.dataset.city === 'other') { win.classList.add('other'); form.querySelector('input').focus(); return; }
    set(t.dataset.city); close();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && back.classList.contains('open')) close(); });
  document.addEventListener('click', function (e) { if (e.target.closest('.js-city-btn')) open(); });
  paint();
  window.CITY = { current: function () { return cur; }, onChange: function (fn) { subs.push(fn); }, open: open };
})();
