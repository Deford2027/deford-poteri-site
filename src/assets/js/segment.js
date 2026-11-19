/* Страница сегмента и раздела: счётчик в первом экране, карточки потерь по разделам, калькулятор. */
(function () {
  var P = window.POTERI, C = window.CITY, fmt = P.fmt, N = P.D.niches;
  var checks = {}, off = {}, $ = function (id) { return document.getElementById(id); };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  N.forEach(function (n) { n.services.forEach(function (s) { if (s[3] === 'sub') off[s[0]] = true; }); });
  var nicheSel = $('niche'), opts = N.map(function (n) { return '<option value="' + n.id + '">' + esc(n.name) + '</option>'; }).join('');
  nicheSel.innerHTML = opts; $('f-niche').innerHTML = opts;

  function drawTop() {
    var r = C.current(), hot = P.cityTotal(r, 'none').hot, dp = P.dayPart();
    document.querySelectorAll('.js-city-in').forEach(function (e) { e.textContent = P.CITY_IN[r]; });
    document.querySelectorAll('.js-src').forEach(function (e) { e.textContent = 'Источник: ' + P.src(r); });
    document.querySelectorAll('.js-cur').forEach(function (e) { e.textContent = P.sign(r); });
    document.querySelectorAll('.js-month').forEach(function (e) { e.textContent = fmt(hot); });
    // Счётчик: горячие поиски за прошедшую часть дня, которые ушли на сайты в топе.
    $('today').textContent = fmt(hot * P.MODEL.servis.sites / 30 * dp.part);
    $('today-l').textContent = dp.label;
  }
  function drawNiches() {
    var r = C.current();
    var cards = N.map(function (n) { var rows = P.nicheRows(n, r, 'none'); return { n: n, rows: rows, t: P.sum(rows.filter(function (x) { return !x.sub; })) }; })
      .sort(function (a, b) { return b.t.money - a.t.money; });
    var wide = window.matchMedia('(min-width: 761px)').matches;
    $('niches').innerHTML = cards.map(function (c, i) {
      // на телефоне разделы свёрнуты до названия и суммы (открыт первый), на широком экране раскрыты
      return '<details class="card niche' + (i === 0 && cards.length > 1 ? ' card--dark' : '') + '"' + (wide || i === 0 ? ' open' : '') + '><summary><h3>' + esc(c.n.name) + '</h3>' +
        '<div class="lose"><b>' + P.money(c.t.money, r) + '</b><span>в месяц проходит мимо без сайта в поиске</span></div></summary>' +
        '<p class="niche__meta">' + fmt(c.t.hot) + ' горячих поисков в месяц · клиентов ≈ ' + P.num(c.t.clients) + '</p>' +
        (c.n.note ? '<p class="niche__note">' + esc(c.n.note) + '</p>' : '') +
        '<table class="mini"><thead><tr><th>Услуга</th><th class="n">Ищут</th><th class="n">Мимо вас</th></tr></thead><tbody>' +
        c.rows.map(function (x) { return '<tr><td>' + esc(x.name) + '</td><td class="n">' + fmt(x.hot) + '</td><td class="n">' + P.money(x.money, r) + '</td></tr>'; }).join('') +
        '</tbody></table><div class="actions">' +
        (c.rows.length > 3 ? '<button class="btn btn--sm ' + (i === 0 && cards.length > 1 ? 'btn--ghost on-dark' : 'btn--white') + ' js-all" type="button" data-n="' + c.rows.length + '">Смотреть все ' + c.rows.length + '</button>' : '') +
        '<a class="btn btn--sm" href="#kalkulyator" data-pick="' + c.n.id + '">Посчитать мою</a></div></details>';
    }).join('');
  }
  var MARK = { '': '', est: '<b class="mark" title="оценка: цен в прайсах города не нашли">*</b>', weak: '<b class="mark" title="цена «от», только работа или один прайс – нижняя граница">°</b>' };
  function niche() { return N.filter(function (n) { return n.id === nicheSel.value; })[0]; }
  function drawChips() {
    var r = C.current(), notes = niche().services.map(function (s) { return P.checkNote(s, r); });
    $('chk-src').textContent = P.hasPrices(r) ? 'чек – медиана прайсов города, впишите свой' : 'чек – оценка по рынку, впишите свой';
    $('est').hidden = notes.indexOf('est') < 0; $('weak').hidden = notes.indexOf('weak') < 0;
    $('chips').innerHTML = niche().services.map(function (s) {
      var v = checks[s[0]] != null ? checks[s[0]] : P.baseCheck(s, r);
      return '<label><input class="cbox" type="checkbox"' + (off[s[0]] ? '' : ' checked') + ' data-q="' + esc(s[0]) + '"><span>' + esc(s[1]) + '</span>' +
        '<span class="chk-wrap"><input class="p-chk" type="number" min="0" step="10" value="' + v + '" data-c="' + esc(s[0]) + '" aria-label="Средний чек: ' + esc(s[1]) + '">' +
        P.sign(r) + MARK[checks[s[0]] != null ? '' : P.checkNote(s, r)] + '</span></label>';
    }).join('');
  }
  function drawCalc() {
    var rows = P.nicheRows(niche(), C.current(), $('state').value, checks).filter(function (x) { return !off[x.q]; }), t = P.sum(rows);
    $('r-cl').textContent = P.num(t.clients);
    $('r-m').textContent = fmt(t.money);
    $('r-d').textContent = fmt(t.money / 30);
    $('r-y').textContent = fmt(t.money * 12);
  }
  $('niches').addEventListener('click', function (e) {
    var all = e.target.closest('.js-all'), pick = e.target.closest('[data-pick]');
    if (all) { var card = all.closest('.niche'); card.classList.toggle('open'); all.textContent = card.classList.contains('open') ? 'Свернуть' : 'Смотреть все ' + all.dataset.n; }
    if (pick) { nicheSel.value = pick.dataset.pick; $('f-niche').value = pick.dataset.pick; drawChips(); drawCalc(); }
  });
  $('chips').addEventListener('change', function (e) { if (e.target.dataset.q) { off[e.target.dataset.q] = !e.target.checked; drawCalc(); } });
  $('chips').addEventListener('input', function (e) {
    var q = e.target.dataset.c; if (!q) return;
    var v = parseInt(e.target.value, 10), mark = e.target.parentNode.querySelector('.mark'); checks[q] = v > 0 ? v : 0;
    if (mark) mark.remove(); // чек вписан руками – это уже не оценка
    drawCalc();
  });
  nicheSel.addEventListener('change', function () { $('f-niche').value = nicheSel.value; drawChips(); drawCalc(); });
  $('state').addEventListener('change', drawCalc);
  function drawAll() { drawTop(); drawNiches(); drawCalc(); }
  // все города Беларуси в BYN – вписанные чеки при смене города сохраняем (как в прототипе)
  C.onChange(function () { drawChips(); drawAll(); });
  drawChips(); drawAll(); setInterval(drawTop, 20000);
})();
