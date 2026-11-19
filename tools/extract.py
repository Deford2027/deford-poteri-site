"""Извлекает тексты и данные из скачанного прототипа (tema-mail.github.io/deford-poteri/by/)
в content/content.json и content/data/<сегмент>.json.

Запуск: python3 -I tools/extract.py <папка_со_скачанным_прототипом>
В папке ожидаются: proto_index.html (страница /by/) и all/<сегмент>/{index.html,data.js,uslugi/index.html,<раздел>/index.html}.
"""
import json
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content"


def read(p):
    return (SRC / p).read_text(encoding="utf-8")


def one(pattern, s, name):
    m = re.search(pattern, s, re.S)
    if not m:
        raise SystemExit(f"не найдено: {name}")
    return m.group(1).strip()


def seo(s):
    d = json.loads(one(r'<script type="application/json" id="w-seo">(.*?)</script>', s, "seo"))
    return {"title": d["title"], "description": d["description"]}


def page_texts(s):
    """Переменные тексты страницы сегмента / раздела (остальное в шаблоне одинаковое)."""
    states = re.findall(r'<article class="w-card"><h3>(.*?)</h3><p>(.*?)</p></article>', s)
    insta = re.search(r"<details><summary>(У меня есть Instagram[^<]*)</summary><p>(.*?)</p></details>", s)
    return {
        "seo": seo(s),
        "h1": one(r"<h1>(.*?)</h1>", s, "h1"),
        # абзац героя: оставляем только текст после «раз в месяц в Яндексе и Google:»
        "hero_list": one(r"раз в месяц в Яндексе и Google: (.*?)\. Это люди", s, "hero"),
        "razdely_h2": one(r'data-name="Разделы".*?<h2>(.*?)</h2>', s, "razdely"),
        "formula": one(r'<p class="p-formula">(.*?)</p>', s, "formula"),
        "state_none": states[0][1],
        "state_landing": states[1][1],
        "step1": one(r"<li><b>Человек ищет</b><span>(.*?)</span></li>", s, "step1"),
        "case_title": one(r'Скрин Метрики: звонки и заявки из поиска</div><h3>(.*?)</h3>', s, "case"),
        "insta_a": insta.group(2),
    }


def load_data(seg):
    t = read(f"all/{seg}/data.js").strip()
    if not t.startswith("window.DATA="):
        raise SystemExit(f"неожиданный формат data.js: {seg}")
    return json.loads(t[len("window.DATA="):].rstrip(";"))


def main():
    idx = read("proto_index.html")
    summary = json.loads(one(r"window\.SUMMARY=(\{.*?\});</script>", idx, "summary"))
    content = {
        "index": {
            "seo": seo(idx),
            "h1": one(r"<h1>(.*?)</h1>", idx, "index h1"),
            "method": one(r'<p class="w-muted">(Спрос – Вордстат.*?)</p>', idx, "index method"),
        },
        "summary": summary,
        "segments": [],
    }
    for sg in summary["segments"]:
        sid = sg["id"]
        seg_html = read(f"all/{sid}/index.html")
        usl_html = read(f"all/{sid}/uslugi/index.html")
        seg = {"id": sid, "name": sg["name"], "short": sg["short"], **page_texts(seg_html),
               "uslugi_seo": seo(usl_html), "niches": []}
        for n in sg["niches"]:
            nh = read(f"all/{sid}/{n['id']}/index.html")
            seg["niches"].append({"id": n["id"], "name": n["name"], **page_texts(nh)})
        content["segments"].append(seg)
        data = load_data(sid)
        (OUT / "data" / f"{sid}.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (OUT / "content.json").write_text(json.dumps(content, ensure_ascii=False, indent=1), encoding="utf-8")
    print("сегментов:", len(content["segments"]), "разделов:", sum(len(s["niches"]) for s in content["segments"]))


if __name__ == "__main__":
    main()
