/* Главная /by/: город кнопками, сумма потерь, топ сегментов, карточки сегментов и таблица всех разделов.
   Данные – window.SUMMARY (summary.js): по каждому разделу и городу [горячих поисков, клиентов, BYN в месяц]. */
(function () {
  var S = window.SUMMARY, KEY = 'poteri-city', $ = function (id) { return document.getElementById(id); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var saved = store.get(KEY), cur = saved && S.regions[saved] ? saved : 'mnsk';
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var fmt = function (n) { return Math.round(n).toLocaleString('ru-RU'); };
  var money = function (n) { return n >= 999500 ? (Math.round(n / 1e5) / 10).toLocaleString('ru-RU') + ' млн BYN' : n >= 1e4 ? fmt(n / 1000) + ' тыс. BYN' : fmt(n) + ' BYN'; };
  var arr = '<span class="btn__arr" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M8 7h9v9"/></svg></span>';

  $('cities').innerHTML = Object.keys(S.regions).map(function (r) { return '<button type="button" data-r="' + r + '">' + esc(S.regions[r]) + '</button>'; }).join('');
  function draw() {
    document.querySelectorAll('#cities [data-r]').forEach(function (b) { b.classList.toggle('on', b.dataset.r === cur); b.setAttribute('aria-pressed', b.dataset.r === cur); });
    document.querySelectorAll('.js-in').forEach(function (e) { e.textContent = S.cityIn[cur]; });
    var segs = S.segments.map(function (s) {
      var ns = s.niches.map(function (n) { return { id: n.id, name: n.name, hot: n.t[cur][0], m: n.t[cur][2], seg: s }; }).sort(function (a, b) { return b.m - a.m; });
      return { s: s, ns: ns, hot: ns.reduce(function (t, n) { return t + n.hot; }, 0), m: ns.reduce(function (t, n) { return t + n.m; }, 0) };
    }).sort(function (a, b) { return b.m - a.m; });
    var tm = segs.reduce(function (t, s) { return t + s.m; }, 0), th = segs.reduce(function (t, s) { return t + s.hot; }, 0);
    $('big').textContent = money(tm); $('hot').textContent = fmt(th);
    $('top').innerHTML = segs.slice(0, 4).map(function (x, i) {
      return '<a class="top-item" href="' + x.s.id + '/"><span class="top-item__n">' + (i + 1) + '</span><span class="top-item__name">' + esc(x.s.name) + '</span><span class="top-item__sum">' + money(x.m) + '</span></a>';
    }).join('');
    $('segs').innerHTML = segs.map(function (x, i) {
      var dark = i === 0;
      return '<article class="card seg-card' + (dark ? ' card--dark' : '') + '"><div class="seg-card__top"><h3><a href="' + x.s.id + '/">' + esc(x.s.name) + '</a></h3><span class="seg-card__tag">' + x.ns.length + ' разд.</span></div>' +
        '<div class="lose"><b>' + money(x.m) + '</b><span>в месяц мимо · ищут ' + fmt(x.hot) + ' раз</span></div><ul class="seg-list">' +
        x.ns.map(function (n) { return '<li><a href="' + x.s.id + '/' + n.id + '/">' + esc(n.name) + '</a><span>' + money(n.m) + '</span></li>'; }).join('') +
        '</ul><div class="actions"><a class="btn btn--sm btn--arrow" href="' + x.s.id + '/">Открыть сегмент' + arr + '</a><a class="link-arrow" href="' + x.s.id + '/uslugi/">Все услуги →</a></div></article>';
    }).join('');
    var all = []; segs.forEach(function (x) { all = all.concat(x.ns); }); all.sort(function (a, b) { return b.m - a.m; });
    document.querySelector('#all tbody').innerHTML = all.map(function (n, i) {
      return '<tr><td class="rank">' + (i + 1) + '</td><td><a href="' + n.seg.id + '/' + n.id + '/">' + esc(n.name) + '</a><small>' + esc(n.seg.short) + '</small></td><td class="n">' + fmt(n.hot) + '</td><td class="n"><b>' + money(n.m) + '</b></td></tr>';
    }).join('');
  }
  $('cities').addEventListener('click', function (e) { var b = e.target.closest('[data-r]'); if (b) { cur = b.dataset.r; store.set(KEY, cur); draw(); } });
  draw();
})();
