"""Собирает сайт в site/ из content/ (тексты и данные прототипа) и src/assets/ (стили, скрипты, картинки).

Структура как в прототипе:
  /by/                         – все ниши Беларуси (8 сегментов, 54 раздела)
  /by/<сегмент>/               – сегмент: потери по разделам, калькулятор, заявка
  /by/<сегмент>/uslugi/        – все услуги сегмента и поиск
  /by/<сегмент>/<раздел>/      – раздел: та же страница, отфильтрованная по разделу

Запуск: python3 -I tools/build.py
"""
import json
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = json.loads((ROOT / "content" / "content.json").read_text(encoding="utf-8"))
OUT = ROOT / "site"

PHONE = "+7 953 777-78-91"
PHONE_HREF = "tel:+79537777891"
TG = "https://t.me/Artem1Galimov"
MAX = "https://max.ru/u/f9LHodD0cOKS6C3PPXRh8eHyRKrJiSTUcpsOsnbQDl6Cp3LSE-Xu-dNig7c"
YEAR = "2026"

e = lambda t: escape(str(t), quote=True)

# ---------- иконки ----------
ARR = ('<span class="btn__arr" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
       'stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M8 7h9v9"/></svg></span>')
I_TG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.4 4.3 2.9 11.4c-1.3.5-1.2 1.2-.2 1.5l4.7 1.5 1.8 5.6c.2.6.4.8.8.8.4 0 '
        '.6-.2.9-.5l2.3-2.2 4.8 3.5c.9.5 1.5.2 1.7-.8l3.1-14.6c.3-1.3-.5-1.9-1.4-1.5ZM9.6 14.6l-.4 4-1.4-4.6 10.5-6.6-8.7 7.2Z"/></svg>')
I_MAX = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5c5.5 0 9.5 3.9 9.5 9.1s-4 9.1-9.5 9.1c-1.3 0-2.6-.2-3.7-.6L4 21.5l1.1-3.9C3.4 16 2.5 13.9 2.5 11.6 '
         '2.5 6.4 6.5 2.5 12 2.5Zm-4 7.6a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3Zm4 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3Zm4 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3Z"/></svg>')
I_PHONE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>')
I_OK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>')
I_STATE = [
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="3"/><path d="M8 8h8M8 12h5"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5M8 11h6"/></svg>',
]


def btn(text, href, cls="", arrow=True):
    return f'<a class="btn{" btn--arrow" if arrow else ""} {cls}" href="{href}">{text}{ARR if arrow else ""}</a>'


# ---------- общие куски ----------
def head(title, desc, root, extra=""):
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta name="theme-color" content="#111111">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
{extra}</head>
<body>
"""


def header(by, nav, cta_text, cta_href):
    links = "".join(f'<a href="{h}">{t}</a>' for t, h in nav)
    return f"""<header class="header">
  <div class="wrap header__in">
    <div class="header__left" style="display:flex;align-items:center;gap:20px">
      <a class="logo" href="{by}" aria-label="Дефорд – на главную"><span class="logo__word">deford</span><span class="logo__dot"></span></a>
      <div class="socials"><a class="soc" href="{TG}" target="_blank" rel="noopener" aria-label="Telegram">{I_TG}</a><a class="soc" href="{MAX}" target="_blank" rel="noopener" aria-label="Макс">{I_MAX}</a></div>
    </div>
    <nav class="nav" aria-label="Разделы страницы">{links}</nav>
    <div class="header__right">
      <a class="header__phone" href="{PHONE_HREF}">{PHONE}</a>
      <a class="btn" href="{cta_href}">{cta_text}</a>
    </div>
  </div>
</header>
"""


def crumbs(items):
    parts = []
    for i, (t, h) in enumerate(items):
        if i:
            parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{h}">{e(t)}</a>' if h else f'<span aria-current="page">{e(t)}</span>')
    return f'<nav class="crumbs" aria-label="Навигация">{"".join(parts)}</nav>'


def footer(by):
    segs = "".join(f'<li><a href="{by}{s["id"]}/">{e(s["name"])}</a></li>' for s in CONTENT["segments"])
    return f"""<footer class="footer" id="kontakty">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__about">
        <a class="logo" href="{by}"><span class="logo__word">deford</span><span class="logo__dot"></span></a>
        <p>Сайты, которые приводят клиентов из поиска. Страница под каждую услугу – в Яндексе и Google. Беларусь.</p>
        <div class="socials"><a class="soc soc--blue" href="{TG}" target="_blank" rel="noopener" aria-label="Telegram">{I_TG}</a><a class="soc" href="{MAX}" target="_blank" rel="noopener" aria-label="Макс">{I_MAX}</a></div>
      </div>
      <div><h4>Ниши</h4><ul>{segs}</ul></div>
      <div><h4>Связаться</h4><ul>
        <li><a class="footer__phone" href="{PHONE_HREF}">{PHONE}</a></li>
        <li><a href="{TG}" target="_blank" rel="noopener">Telegram</a></li>
        <li><a href="{MAX}" target="_blank" rel="noopener">Макс</a></li>
      </ul></div>
    </div>
    <div class="footer__bottom">
      <span>© Дефорд, {YEAR}</span>
      <span><a href="#">Политика конфиденциальности</a> · <a href="#">Согласие на обработку данных</a></span>
    </div>
  </div>
</footer>
"""


def sticky(second_text, second_href):
    return (f'<div class="sticky-bar"><a class="btn" href="{PHONE_HREF}">Позвонить</a>'
            f'<a class="btn btn--ghost" href="{second_href}">{second_text}</a></div>\n')


def page_end(scripts):
    tags = "".join(f'<script src="{s}"></script>\n' for s in scripts)
    return tags + "</body>\n</html>\n"


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>\n"


ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Дефорд", "telephone": PHONE.replace(" ", ""),
       "sameAs": [TG], "description": "Сайты, которые приводят клиентов из поиска – Беларусь"}


# ---------- /by/ ----------
def build_index():
    c = CONTENT["index"]
    by, root = "", "../"
    html = head(c["seo"]["title"], c["seo"]["description"], root, jsonld(ORG))
    html += '<section class="hero">\n'
    html += header(by, [("Сегменты", "#segmenty"), ("Все разделы", "#razdely"), ("Контакты", "#kontakty")], "Выбрать нишу", "#segmenty")
    html += f"""  <div class="wrap">
    <div class="hero__grid">
      <div class="hero__main">
        <div class="seg-ctl" id="cities" role="group" aria-label="Город"></div>
        <h1>{c["h1"]}</h1>
        <div class="big-sum"><span id="big">…</span><br><span style="font-size:.5em;letter-spacing:-.04em">в месяц</span></div>
        <p class="hero__p">В <b class="js-in">Минске</b> услуги и товары этих ниш ищут <b id="hot">…</b> раз в месяц в Яндексе и Google. Сумма выше – сколько из этого получают те, у кого сайт со страницей под услугу стоит в топе, если у вас такого сайта нет.</p>
        <p class="hero__hint">Витебск, Гродно, Могилёв – снимем по заявке: «Другой город» на странице сегмента.</p>
        <div class="actions on-dark">{btn("Найти свою нишу", "#segmenty")}{btn("Все разделы по деньгам", "#razdely", "btn--ghost", False)}</div>
      </div>
      <div class="glass top-list" aria-live="polite">
        <div class="top-list__head"><span>Больше всего теряют в <span class="js-in">Минске</span></span><span>BYN / мес</span></div>
        <div class="top-list" id="top"></div>
      </div>
    </div>
  </div>
</section>
<main>
  <section class="section" id="segmenty">
    <div class="wrap">
      <div class="section__head section__head--split">
        <h2>Сегменты и разделы</h2>
        <p class="lead">Найдите свою нишу. У каждого сегмента и каждого раздела – своя страница с калькулятором потерь по вашим услугам и чеку. Порядок – по сумме потерь в выбранном городе.</p>
      </div>
      <div class="grid" id="segs" style="--cols:2"></div>
    </div>
  </section>
  <section class="section" id="razdely">
    <div class="wrap">
      <div class="panel">
        <div class="section__head section__head--split">
          <h2>Все разделы по деньгам</h2>
          <p class="lead">54 раздела по 8 сегментам – от самых денежных к остальным. Нажмите на раздел, чтобы посчитать потери по своим услугам.</p>
        </div>
        <div class="table-wrap"><table class="table" id="all"><thead><tr><th class="rank">#</th><th>Раздел</th><th class="n">Ищут в месяц</th><th class="n">Мимо, BYN/мес</th></tr></thead><tbody></tbody></table></div>
        <p class="table-note">Спрос – Вордстат Яндекса за октябрь 2026 по городу × 2,5 (доля Google в Беларуси). Чеки – медианы прайсов Минска, где не нашли – оценка. Как считаем – в калькуляторе на странице сегмента.</p>
      </div>
    </div>
  </section>
</main>
"""
    html += footer(by)
    html += sticky("Выбрать нишу", "#segmenty")
    html += page_end(["summary.js", f"{root}assets/js/index.js", f"{root}assets/js/site.js"])
    write("by/index.html", html)
    write("by/summary.js", "window.SUMMARY=" + json.dumps(CONTENT["summary"], ensure_ascii=False, separators=(",", ":")) + ";\n")


# ---------- сегмент и раздел ----------
FAQ_CONST = [
    ("У меня и так клиенты по сарафану, зачем мне сайт?", "Сарафан не растёт по заказу. Сайт даёт поток на дорогие работы вашей ниши круглый год, а не только то, что и так идёт по знакомым."),
    None,  # Instagram – свой ответ на каждой странице
    ("Когда пойдут клиенты из поиска?", "Срок зависит от ниши и конкуренции в вашем городе – назовём его после разбора. До этого заявки дают карты и реклама."),
    ("Моего города нет в списке", "Снимем спрос по вашему городу и нише по заявке и пришлём расчёт. Нажмите на город вверху страницы и выберите «Другой город»."),
    ("Откуда цены?", "Медиана цен из прайсов компаний Минска. Где прайсов не нашли – оценка, она помечена. Впишите свой средний чек – и увидите свою цифру."),
    ("Откуда цифры спроса?", "Статистика запросов Яндекса по вашему городу за прошлый месяц, плюс Google: в Беларуси он больше половины поиска, его досчитываем по доле поисковиков. Убираем «своими руками», «бесплатно», «вакансии» и прочие не-покупательские запросы."),
]


def faq_items(p):
    out = []
    for item in FAQ_CONST:
        out.append(("У меня есть Instagram – этого мало?", p["insta_a"]) if item is None else item)
    return out


def build_seg_page(seg, niche=None):
    p = niche or seg
    by = "../../" if niche else "../"
    root = "../../../" if niche else "../../"
    usl = "../uslugi/" if niche else "uslugi/"
    data_src = "../data.js" if niche else "data.js"
    faqs = faq_items(p)
    ld = jsonld(ORG) + jsonld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    html = head(p["seo"]["title"], p["seo"]["description"], root, ld)

    cr = [("Беларусь", by), (seg["name"], "../" if niche else None)]
    if niche:
        cr.append((niche["name"], None))
    if niche:
        others = [n for n in seg["niches"] if n["id"] != niche["id"]]
        chips = "".join(f'<a class="chip" href="../{n["id"]}/">{e(n["name"])}</a>' for n in others)
    else:
        chips = "".join(f'<a class="chip" href="{n["id"]}/">{e(n["name"])}</a>' for n in seg["niches"])
    chips += f'<a class="chip" href="{usl}" style="background:var(--blue-soft);color:var(--blue)">Все услуги и поиск</a>'
    h2_loss = "Сколько клиентов и денег проходит мимо – по услугам раздела" if niche else "Сколько клиентов и денег проходит мимо – по разделам"

    html += '<section class="hero">\n'
    html += header(by, [("Потери", "#nishi"), ("Калькулятор", "#kalkulyator"), ("Как работает", "#kak"), ("Вопросы", "#faq")],
                   '<span>Посчитать<span class="long"> потери</span></span>', "#kalkulyator")
    html += f"""  <div class="wrap">
    {crumbs(cr)}
    <div class="hero__grid">
      <div class="hero__main">
        <div class="pill-row"><span class="muted">Ваш город:</span><button class="city-btn js-city-btn" type="button">Минск ▾</button></div>
        <h1>{p["h1"]}</h1>
        <p class="hero__p">В <b class="js-city-in">Минске</b> ваши услуги ищут <b class="js-month">…</b> раз в месяц в Яндексе и Google: {p["hero_list"]}. Это люди с задачей и деньгами. Они звонят тем, кого нашли в поиске. Нет сайта со страницей под их услугу – звонят не вам.</p>
        <ul class="hero__ticks">
          <li><span><b>Горячие</b> – ищут, кто сделает, а не «как сделать своими руками»</span></li>
          <li><span><b>Бесплатные</b> – клиент из поиска не стоит денег за клик, как в рекламе</span></li>
          <li><span><b>Каждый день</b> – спрос не заканчивается, его забирают конкуренты</span></li>
        </ul>
        <div class="actions on-dark">{btn("Сколько теряет моя ниша", "#nishi")}{btn("Найти свою услугу", usl, "btn--ghost", False)}</div>
        <p class="hero__hint">Расчёт – на статистике поиска по вашему городу, без звонка и регистрации</p>
      </div>
      <div class="glass counter" aria-live="polite">
        <span class="counter__label"><span id="today-l">Сегодня с 8:00</span> в <span class="js-city-in">Минске</span> бизнес без сайта в поиске упустил</span>
        <span class="counter__num" id="today">…</span>
        <span class="counter__cap">горячих поисков ваших услуг</span>
        <span class="counter__live">Счётчик идёт в течение дня</span>
      </div>
    </div>
  </div>
</section>
<main>
  <section class="section">
    <div class="wrap">
      <div class="section__head"><span class="tag">{"Раздел сегмента" if niche else "Разделы"}</span><h2>{p["razdely_h2"]}</h2></div>
      <div class="chips">{chips}</div>
    </div>
  </section>

  <section class="section" id="nishi">
    <div class="wrap">
      <div class="section__head section__head--split">
        <h2>{h2_loss}</h2>
        <div class="stack">
          <div class="pill-row light"><span class="muted">Город:</span><button class="city-btn js-city-btn" type="button">Минск ▾</button></div>
          <p class="lead">Найдите свой раздел. В карточке – три самые искомые услуги, «Смотреть все» покажет все. Сумма – сколько в месяц уходит тем, у кого сайт стоит в топе, если у вас сайта нет.</p>
          <p class="muted js-src" style="font-size:13px"></p>
        </div>
      </div>
      <div class="grid" id="niches" style="--cols:3"></div>
    </div>
  </section>

  <section class="section section--strip">
    <div class="wrap"><div class="cta"><p>Не нашли свою услугу? Вбейте её в поиск – покажем, сколько клиентов вы теряете именно на ней</p>{btn("Все услуги и поиск", usl, "btn--white")}</div></div>
  </section>

  <section class="section" id="kalkulyator">
    <div class="wrap">
      <div class="section__head section__head--split">
        <h2>Посчитайте по своим услугам и своему чеку</h2>
        <p class="lead">Выберите раздел и что у вас сейчас, снимите лишние услуги и впишите свой средний чек – пересчёт сразу.</p>
      </div>
      <div class="panel">
        <div class="calc">
          <div class="calc__form">
            <div class="calc__row">
              <label class="field"><span><span class="field__n">1.</span> Раздел</span><select class="select" id="niche"></select></label>
              <label class="field"><span><span class="field__n">2.</span> Что у вас сейчас</span><select class="select" id="state"><option value="none">Сайта нет</option><option value="landing">Есть лендинг на одну страницу</option><option value="weak">Сайт есть, но не продвигается</option></select></label>
            </div>
            <div class="svc-head"><b><span class="field__n">3.</span> Ваши услуги</b><span class="muted">снимите лишние; <span id="chk-src">чек – оценка по рынку, впишите свой</span></span></div>
            <div class="svc" id="chips"></div>
            <div class="calc__notes">
              <p id="est" hidden>* – оценка: цен на эту услугу в прайсах города не нашли</p>
              <p id="weak" hidden>° – в прайсах цена «от» или только работа без запчастей: это нижняя граница, ваш реальный чек выше</p>
            </div>
            <details class="how"><summary>Как считаем</summary>
              <p class="formula">{p["formula"]}</p>
            </details>
          </div>
          <div class="card card--dark result" aria-live="polite">
            <div class="result__main"><b id="r-m">…</b><span><span class="js-cur">BYN</span> в месяц выручки проходит мимо вас</span></div>
            <div class="result__grid">
              <div class="result__cell"><b id="r-cl">…</b><span>клиентов в месяц уходят к другим</span></div>
              <div class="result__cell"><b id="r-d">…</b><span><span class="js-cur">BYN</span> в день</span></div>
              <div class="result__cell result__cell--wide"><b id="r-y">…</b><span><span class="js-cur">BYN</span> за год</span></div>
            </div>
            {btn("Получить точный расчёт", "#zayavka", "btn--block")}
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--strip">
    <div class="wrap"><div class="cta cta--dark"><p>Пришлём расчёт по вашему бизнесу: ваши услуги и город – и кто из конкурентов забирает этих клиентов</p>{btn("Получить расчёт", "#zayavka")}</div></div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head"><span class="tag">Почему нет клиентов из поиска</span><h2>Карты, Instagram, лендинг и «просто сайт» не ловят поиск по услугам</h2></div>
      <div class="grid states" style="--cols:3">
        <article class="card"><span class="states__icon">{I_STATE[0]}</span><h3>Сайта нет</h3><p>{p["state_none"]}</p></article>
        <article class="card card--dark"><span class="states__icon">{I_STATE[1]}</span><h3>Лендинг на одну страницу</h3><p>{p["state_landing"]}</p></article>
        <article class="card"><span class="states__icon">{I_STATE[2]}</span><h3>Сайт без продвижения</h3><p>Страницы есть, но стоят на третьей странице выдачи. Туда доходит 1 человек из 100. Сайт есть – клиентов с него нет.</p></article>
      </div>
    </div>
  </section>

  <section class="section" id="kak">
    <div class="wrap">
      <div class="section__head"><span class="tag">Как это работает</span><h2>Страница под каждую услугу – и каждая ловит свой запрос в Яндексе и Google</h2></div>
      <ol class="steps">
        <li><b>Человек ищет</b><span>{p["step1"]}</span></li>
        <li><b>Видит вашу страницу</b><span>/services/&lt;услуга&gt;/ – цена, сроки, гарантия, фото работ</span></li>
        <li><b>Звонит или пишет</b><span>кнопка звонка, Viber, Telegram, заявка</span></li>
        <li><b>Видите в кабинете</b><span>откуда пришёл и с какой страницы</span></li>
      </ol>
      <div class="schema">
        <div class="schema__img"><img src="{root}assets/img/schema.webp" width="780" height="448" loading="lazy" alt="Схема сайта: главная, разделы и услуги, работы с фото и ценами"></div>
        <div class="schema__txt">
          <h3>Сайт под спрос вашего города</h3>
          <div class="schema__path"><span>Главная</span><i>→</i><span>Разделы и услуги</span><i>→</i><span>Работы с фото и ценами</span></div>
          <p class="muted">Каждая страница – свой запрос из карточек выше. В Беларуси Google – больше половины поиска: страницы делаем под оба поисковика, спрос на странице уже посчитан по обоим.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head section__head--split">
        <h2>В рекламе за этого же клиента платите каждый раз. Из поиска он приходит бесплатно</h2>
        <p class="lead">Реклама нужна для быстрого старта, пока сайт растёт: заявки с первой недели. Но за каждый клик вы платите – и чем дороже ниша, тем дороже клик. Сайт в топе приводит тех же людей без оплаты за клик – месяц за месяцем.</p>
      </div>
      <div class="versus">
        <div class="card"><span class="versus__k">Реклама</span><p>Заявки с первой недели. Платите за каждый переход – остановили бюджет, остановился поток.</p></div>
        <div class="card card--dark"><span class="versus__k">Поиск</span><p>Сайт в топе приводит тех же людей бесплатно. Поток копится и работает месяц за месяцем.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="panel panel--dark">
        <div class="proof">
          <div class="proof__main">
            <span class="tag" style="color:#8db6ff">Почему нам верить</span>
            <h2>Мы держим свои бизнесы и проверили это на себе</h2>
            <p class="muted" style="max-width:560px">Дефорд основан действующими предпринимателями. Прежде чем продавать сайты из поиска, мы проверили их на своём бизнесе – и считаем деньги так же, как вы.</p>
            <div class="proof__cases">
              <article class="case"><div class="case__img"><img src="{root}assets/img/growth.webp" width="780" height="468" loading="lazy" alt="Заявки из поиска по месяцам"></div><h3>Evolution Car Service, Минск</h3><p>Свой автосервис: заявки из поиска и рост по месяцам покажем на созвоне – с цифрами из Метрики.</p></article>
              <article class="case"><div class="case__img"><img src="{root}assets/img/clients.webp" width="1000" height="368" loading="lazy" alt="Звонки и заявки из поиска"></div><h3>{p["case_title"]}</h3><p>Разберём на созвоне проекты, близкие к вашей нише: какие страницы приводят звонки и заявки.</p></article>
            </div>
          </div>
          <div class="founder">
            <img src="{root}assets/img/founder.webp" width="700" height="1226" loading="lazy" alt="Артём Галимов, основатель Дефорд">
            <div class="founder__card"><a class="soc soc--blue" href="{TG}" target="_blank" rel="noopener" aria-label="Telegram">{I_TG}</a><div><b>Артём Галимов</b><span>Основатель и руководитель Дефорд</span></div></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--strip">
    <div class="wrap"><div class="cta"><p>Разберём ваш сайт, Instagram или карточку на картах: каких страниц не хватает и кто из конкурентов забирает ваших клиентов</p>{btn("Получить разбор", "#zayavka", "btn--white")}</div></div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="price">
        <div class="card stack" style="gap:28px;align-content:start">
          <span class="tag">Цена и состав</span>
          <h2>Сайт с продвижением окупается одним-двумя заказами в месяц</h2>
          <ul class="checklist"><li>Страницы под ваши услуги по спросу вашего города – в Яндексе и Google</li><li>Кабинет заявок: откуда пришёл клиент</li><li>Карты и реклама – заявки с первых недель</li><li>Хостинг в Беларуси по Указу № 60</li><li>Ведение и рост позиций</li></ul>
        </div>
        <div class="card card--white price__card">
          <div class="price__img"><img src="{root}assets/img/stack.webp" width="780" height="448" loading="lazy" alt="Сайт, реклама и аналитика в одной системе"></div>
          <p class="price__in">Стоимость рассчитаем под ваши услуги и город</p>
          {btn("Узнать стоимость", "#zayavka")}
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="faq">
    <div class="wrap faq">
      <div class="faq__side">
        <span class="tag">Вопросы</span>
        <h2>Что спрашивают владельцы</h2>
        <p class="muted">Не нашли ответ – напишите, ответим в Telegram или Макс.</p>
        <div class="actions"><a class="btn btn--ghost" href="{TG}" target="_blank" rel="noopener">{I_TG.replace('aria-hidden="true"', 'aria-hidden="true" width="20" height="20"')} Написать в Telegram</a></div>
      </div>
      <div class="faq__list">
        {"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)}
      </div>
    </div>
  </section>

  <section class="section" id="zayavka">
    <div class="wrap">
      <div class="panel panel--dark">
        <div class="lead-form">
          <div class="lead-form__side">
            <span class="tag" style="color:#8db6ff">Первый шаг</span>
            <h2>Получите расчёт: сколько клиентов уходит от вас</h2>
            <p class="muted">Пришлём расчёт в Telegram или Макс. Подготовьте: список услуг, город, средний чек.</p>
            <div class="contacts">
              <a href="{PHONE_HREF}"><span class="soc">{I_PHONE}</span>{PHONE}</a>
              <a href="{TG}" target="_blank" rel="noopener"><span class="soc soc--blue">{I_TG}</span>Telegram</a>
              <a href="{MAX}" target="_blank" rel="noopener"><span class="soc">{I_MAX}</span>Макс</a>
            </div>
          </div>
          <form class="form js-form" novalidate>
            <label class="field">Имя<input class="input" name="name" autocomplete="name" required></label>
            <label class="field">Телефон<input class="input" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+375 (__) ___-__-__" required></label>
            <label class="field">Раздел<select class="select" id="f-niche" name="niche"></select></label>
            <label class="field">Сайт или название<input class="input" name="site"></label>
            <label class="check"><input class="cbox" type="checkbox" data-agree> <span>Согласен на обработку <a href="#">персональных данных</a></span></label>
            <button class="btn btn--block" type="submit" disabled>Получить расчёт</button>
            <p class="form__hint">Пришлём расчёт в Telegram или Макс</p>
            <div class="form__ok">
              <div class="form__ok-icon">{I_OK}</div>
              <h3>Заявка принята</h3>
              <p class="muted">Расчёт пришлём в Telegram или Макс. Подготовьте: список услуг, город, средний чек.</p>
              <p class="muted">Срочно – <a href="{PHONE_HREF}">позвонить</a> или <a href="{TG}" target="_blank" rel="noopener">написать в Telegram</a>.</p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</main>
"""
    html += footer(by)
    html += sticky("Посчитать", "#kalkulyator")
    scripts = [data_src]
    if niche:
        html += f'<script src="{data_src}"></script>\n<script>window.DATA.niches = window.DATA.niches.filter(function (n) {{ return n.id === "{niche["id"]}"; }});</script>\n'
        scripts = []
    html += page_end(scripts + [f"{root}assets/js/calc.js", f"{root}assets/js/city.js", f"{root}assets/js/segment.js", f"{root}assets/js/site.js"])
    path = f"by/{seg['id']}/{niche['id']}/index.html" if niche else f"by/{seg['id']}/index.html"
    write(path, html)


# ---------- все услуги сегмента ----------
def build_uslugi(seg, data):
    by, root = "../../", "../../../"
    names = [s[1] for n in data["niches"] for s in n["services"] if s[3:4] != ["sub"]][:40]
    ph = ", ".join(n.lower() if i else n for i, n in enumerate([names[0], names[len(names) // 3], names[2 * len(names) // 3]])) + "…"
    html = head(seg["uslugi_seo"]["title"], seg["uslugi_seo"]["description"], root, jsonld(ORG))
    html += '<section class="hero">\n'
    html += header(by, [("Потери по разделам", "../#nishi"), ("Калькулятор", "../#kalkulyator"), ("Заявка", "../#zayavka")], "Получить расчёт", "../#zayavka")
    html += f"""  <div class="wrap">
    {crumbs([("Беларусь", by), (seg["name"], "../"), ("Все услуги", None)])}
    <div class="hero__main" style="margin-top:28px;max-width:980px">
      <h1>Вбейте свою услугу – покажем, сколько клиентов вы на ней теряете</h1>
      <div class="pill-row"><span class="muted">Город:</span><button class="city-btn js-city-btn" type="button">Минск ▾</button>
        <label class="pill-row"><span class="muted">Что у вас сейчас:</span><select class="select" id="state"><option value="none">Сайта нет</option><option value="landing">Есть лендинг на одну страницу</option><option value="weak">Сайт есть, но не продвигается</option></select></label></div>
      <div class="search" role="search"><input id="q" type="search" placeholder="{e(ph)}" aria-label="Поиск услуги" autocomplete="off"><button class="btn btn--arrow" id="find" type="button">Найти{ARR}</button></div>
    </div>
  </div>
</section>
<main>
  <section class="section" style="padding-top:clamp(40px,5vw,64px)">
    <div class="wrap stack" style="gap:20px">
      <p class="sum-line" id="sum">…</p>
      <div class="table-wrap card--white" id="tbl-wrap" style="box-shadow:var(--shadow)"><table class="table usl-table" id="tbl"><thead><tr><th>Услуга</th><th class="n">Ищут<span class="hide-m"> в месяц</span></th><th class="n hide-m">Клиентов мимо</th><th class="n">Мимо вас<span class="hide-m"> в месяц</span></th><th class="n"><span class="hide-m">Ваш </span>чек, <span class="js-cur">BYN</span></th></tr></thead><tbody></tbody></table></div>
      <div><button class="btn btn--ghost" id="more" type="button">Показать все услуги</button></div>
      <div class="empty" id="empty" hidden>
        <p><b>Такой услуги в списке пока нет.</b> Оставьте заявку – снимем спрос по ней в вашем городе и пришлём расчёт.</p>
        {btn("Снять спрос по моей услуге", "../#zayavka")}
      </div>
      <div class="actions">{btn("Получить расчёт по моим услугам", "../#zayavka")}{btn("Потери по разделам", "../#nishi", "btn--ghost", False)}</div>
      <p class="muted js-src" style="font-size:13px"></p>
    </div>
  </section>
  <section class="section section--strip">
    <div class="wrap"><div class="cta cta--dark"><p>Пришлём расчёт по всем вашим услугам сразу – и покажем, кто из конкурентов забирает этих клиентов</p>
      <div class="actions">{btn("Получить расчёт", "../#zayavka")}{btn("Потери по разделам", "../#nishi", "btn--ghost on-dark", False)}</div></div></div>
  </section>
</main>
"""
    html += footer(by)
    html += sticky("Расчёт", "../#zayavka")
    html += page_end(["../data.js", f"{root}assets/js/calc.js", f"{root}assets/js/city.js", f"{root}assets/js/uslugi.js", f"{root}assets/js/site.js"])
    write(f"by/{seg['id']}/uslugi/index.html", html)


def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "src" / "assets", OUT / "assets")
    write("index.html", '<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Дефорд</title>'
          '<meta http-equiv="refresh" content="0; url=by/"><link rel="canonical" href="by/"></head>'
          '<body><a href="by/">Перейти на сайт</a></body></html>\n')
    build_index()
    n = 1
    for seg in CONTENT["segments"]:
        data = json.loads((ROOT / "content" / "data" / f"{seg['id']}.json").read_text(encoding="utf-8"))
        write(f"by/{seg['id']}/data.js", "window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
        build_seg_page(seg)
        build_uslugi(seg, data)
        n += 2
        for niche in seg["niches"]:
            build_seg_page(seg, niche)
            n += 1
    print("страниц:", n)


if __name__ == "__main__":
    main()
