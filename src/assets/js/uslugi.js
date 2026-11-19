/* Страница «Все услуги»: поиск услуги, таблица потерь, чек правится прямо в строке. Логика поиска – из прототипа. */
(function () {
  var P = window.POTERI, C = window.CITY, fmt = P.fmt, $ = function (id) { return document.getElementById(id); };
  var checks = {}, showAll = false, LIMIT = 15, last = { keys: {}, searching: false };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var norm = function (s) { return String(s).toLowerCase().replace(/ё/g, 'е').trim(); };
  var toWords = function (s) { return norm(s).split(/[^a-zа-я0-9]+/).filter(Boolean); };
  // Основы слова: без окончания («плёнка» → «пленк») и с беглой гласной («потолок» → «потолк»).
  function stems(w) {
    var s = w.length >= 4 ? w.replace(/(ами|ями|ой|ей|ия|ие|ий|ый|ая|ов|ев|ам|ям|ах|ях|а|я|ы|и|у|ю|е|о|ь|й)$/, '') : w;
    var m = s.match(/^(.+[^аеиоуыэюя])[ое]([^аеиоуыэюя])$/);
    return m ? [s, m[1] + m[2]] : [s];
  }
  function hasWord(w, main, extra) {
    if (w.length < 3) return main.concat(extra).indexOf(w) >= 0;
    return stems(w).some(function (st) {
      return main.some(function (h) { return h.indexOf(st) === 0 || (st.length >= 5 && h.indexOf(st) > 0); }) || extra.some(function (h) { return h.indexOf(st) === 0; });
    });
  }
  var NOTE = { '': '<small class="tag-est js-mark"></small>', est: '<small class="tag-est js-mark" title="цен в прайсах города не нашли">оценка</small>', weak: '<small class="tag-est js-mark" title="в прайсах цена «от», только работа или один прайс – нижняя граница">от</small>' };
  function rows() { return P.allRows(C.current(), $('state').value, checks).sort(function (a, b) { return b.money - a.money; }); }
  // Поиск ступенями: по названию услуги и запросу; пусто – по примерам «как ищут»; пусто – по названию раздела.
  function search(all, words) {
    var by = function (pick) { return all.filter(function (x) { var hay = pick(x); return words.every(function (w) { return hasWord(w, hay[0], hay[1]); }); }); };
    var found = by(function (x) { return [toWords(x.name + ' ' + x.q), []]; });
    if (!found.length) found = by(function (x) { return [[], toWords(x.top.join(' '))]; });
    if (!found.length) found = by(function (x) { return [toWords(x.nicheName), []]; });
    return found;
  }
  function paintSum(found) {
    var r = C.current(), t = P.sum(last.searching ? found : found.filter(function (x) { return !x.sub; }));
    $('sum').innerHTML = found.length ? (last.searching ? 'Найдено услуг: ' : 'Услуг в списке: ') + found.length + ' · в ' + P.CITY_IN[r] +
      ' мимо вас <b>' + P.money(t.money, r) + '</b> в месяц · клиентов ≈ ' + P.num(t.clients) : 'Ничего не нашли по запросу «' + esc($('q').value) + '»';
  }
  function draw() {
    var words = toWords($('q').value), all = rows(), r = C.current();
    var found = words.length ? search(all, words) : all;
    var shown = words.length || showAll ? found : found.slice(0, LIMIT);
    last = { keys: {}, searching: !!words.length }; found.forEach(function (x) { last.keys[x.q] = 1; });
    document.querySelector('#tbl tbody').innerHTML = shown.map(function (x) {
      return '<tr data-q="' + esc(x.q) + '"><td><b>' + esc(x.name) + '</b><small>' + esc(x.nicheName) + '</small></td><td class="n">' + fmt(x.hot) + '</td><td class="n hide-m">' +
        P.num(x.clients) + '</td><td class="n js-m"><b>' + P.money(x.money, r) + '</b></td><td class="n"><input class="p-chk" type="number" min="0" step="10" value="' +
        x.check + '" aria-label="Средний чек: ' + esc(x.name) + '">' + NOTE[checks[x.q] == null ? P.checkNote(x.s, r) : ''] + '</td></tr>';
    }).join('');
    $('tbl-wrap').hidden = !found.length; $('empty').hidden = !!found.length;
    $('more').hidden = !!words.length || found.length <= LIMIT;
    $('more').textContent = showAll ? 'Свернуть' : 'Показать все услуги (' + found.length + ')';
    paintSum(found);
    document.querySelector('.js-src').textContent = 'Источник: ' + P.src(r) + '. «Ищут» – горячие формулировки, без «своими руками» и прочего.';
    document.querySelectorAll('.js-cur').forEach(function (e) { e.textContent = P.sign(r); });
  }
  // Правка чека: поле не перерисовываем – меняем сумму строки и общий итог.
  $('tbl').addEventListener('input', function (e) {
    if (!e.target.classList.contains('p-chk')) return;
    var tr = e.target.closest('tr'), v = parseInt(e.target.value, 10); checks[tr.dataset.q] = v > 0 ? v : 0;
    var all = rows(), x = all.filter(function (r) { return r.q === tr.dataset.q; })[0], mark = tr.querySelector('.js-mark');
    if (mark) mark.textContent = ''; // чек вписан руками – это уже не оценка
    if (x) tr.querySelector('.js-m').innerHTML = '<b>' + P.money(x.money, C.current()) + '</b>';
    paintSum(all.filter(function (r) { return last.keys[r.q]; }));
  });
  $('q').addEventListener('input', draw);
  $('find').addEventListener('click', function () { draw(); $('sum').scrollIntoView({ block: 'start', behavior: 'smooth' }); });
  $('q').addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); $('find').click(); } });
  $('state').addEventListener('change', draw);
  $('more').addEventListener('click', function () { showAll = !showAll; draw(); });
  C.onChange(draw);
  draw();
})();
