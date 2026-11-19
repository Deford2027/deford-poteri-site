/* Модель потерь клиентов без SEO-сайта – перенесена из прототипа без изменений формул.
   Данные – window.DATA (data.js сегмента: Вордстат + доля Google, чеки – медианы прайсов). */
(function () {
  var D = window.DATA;
  var MODEL = {
    servis: { sites: 0.5, top: 0.2, conv: 0.08, close: 0.6 }
  };
  // Своя модель сегмента (магазины – конверсия в заказ, отдых – меньше переходов на сайты) задаётся в data.js.
  if (D.model) Object.keys(D.model).forEach(function (k) { MODEL.servis[k] = D.model[k]; });
  // Сколько потенциала поиска забирает бизнес в каждом состоянии.
  var STATES = {
    none: { name: 'Сайта нет', take: 0 },
    landing: { name: 'Есть лендинг на одну страницу', take: 0.15 },
    weak: { name: 'Сайт есть, но не продвигается', take: 0.1 }
  };
  var CITY_IN = D.cityIn || {};
  var fmt = function (n) { return Math.round(n).toLocaleString('ru-RU'); };
  var sign = function (region) { var c = D.currency && D.currency[region]; return c ? c.sign : 'BYN'; };
  function priced(s, region) { var c = D.checks && D.checks[region]; return c && c[s[0]] ? c[s[0]] : null; }
  function hasPrices(region) { return !!(D.checks && D.checks[region]); }
  // 'est' – оценка (в прайсах города услуги не нашли), 'weak' – один прайс или цена «от», '' – медиана прайсов.
  function checkNote(s, region) {
    if (!s || !hasPrices(region)) return '';
    var p = priced(s, region); if (!p) return 'est';
    return p.n < 2 || p.b === 'ot' ? 'weak' : '';
  }
  function baseCheck(s, region) {
    var p = priced(s, region); if (p) return p.v;
    var c = D.currency && D.currency[region]; if (!c) return s[2];
    var x = s[2] * c.rate, k = Math.pow(10, Math.max(0, Math.floor(Math.log(x) / Math.LN10) - 1));
    return Math.round(x / k) * k;
  }
  var money = function (n, region) {
    var cur = ' ' + sign(region);
    if (n >= 999500) return (Math.round(n / 1e5) / 10).toLocaleString('ru-RU') + ' млн' + cur;
    if (n >= 1e4) return fmt(n / 1000) + ' тыс.' + cur;
    return fmt(n) + cur;
  };
  var num = function (n) { return n < 10 ? (Math.round(n * 10) / 10).toLocaleString('ru-RU') : fmt(n); };
  var get = function (q, r) { var g = D.services[q]; return g && g[r] ? g[r] : null; };

  // Клиентов в месяц у сайта в топ-3. Запросы «рядом» – в основном карты: на сайты уходит вдвое меньше.
  function clients(hot, maps, close) { var m = MODEL.servis; return hot * (maps ? m.sites / 2 : m.sites) * m.top * m.conv * (close || m.close); }
  function lost(potential, state) { return potential * (1 - STATES[state].take); }

  function nicheRows(niche, region, state, checks) {
    return niche.services.map(function (s) {
      var d = get(s[0], region), check = checks && checks[s[0]] != null ? checks[s[0]] : baseCheck(s, region);
      if (!d) return null;
      var cl = lost(clients(d.hot, s[3] === 'maps', niche.close), state || 'none');
      return { q: s[0], s: s, name: s[1], check: check, maps: s[3] === 'maps', sub: s[3] === 'sub', hot: d.hot, top: d.top || [],
        clients: cl, money: cl * check, niche: niche.id, nicheName: niche.short };
    }).filter(Boolean).sort(function (a, b) { return b.hot - a.hot; });
  }
  function sum(rows) {
    return rows.reduce(function (t, x) { t.hot += x.hot; t.clients += x.clients; t.money += x.money; return t; }, { hot: 0, clients: 0, money: 0 });
  }
  // Все услуги города без повторов (одна услуга может входить в два раздела – берём один раз).
  function allRows(region, state, checks) {
    var seen = {}, out = [];
    D.niches.forEach(function (n) {
      nicheRows(n, region, state, checks).forEach(function (x) { if (!seen[x.q]) { seen[x.q] = 1; out.push(x); } });
    });
    return out;
  }
  // Итог города – без услуг с флагом sub (они уже сидят внутри общих запросов).
  function cityTotal(region, state, checks) { return sum(allRows(region, state, checks).filter(function (x) { return !x.sub; })); }
  // До 8 утра показываем вчерашний день целиком.
  function dayPart() {
    var d = new Date(), h = d.getHours() + d.getMinutes() / 60;
    if (h < 8) return { part: 1, label: 'За вчерашний день' };
    return { part: Math.min(1, (h - 8) / 13), label: 'Сегодня с 8:00' };
  }
  window.POTERI = { D: D, MODEL: MODEL, STATES: STATES, CITY_IN: CITY_IN, fmt: fmt, money: money, num: num, sign: sign,
    baseCheck: baseCheck, hasPrices: hasPrices, checkNote: checkNote,
    src: function (region) { return (D.src && D.src[region]) || D.date; },
    nicheRows: nicheRows, allRows: allRows, cityTotal: cityTotal, sum: sum, lost: lost, dayPart: dayPart };
})();
