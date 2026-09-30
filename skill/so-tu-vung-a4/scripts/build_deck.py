#!/usr/bin/env python3
"""Build a ready-to-use Sổ Từ Vựng A4 HTML file with a vocabulary deck baked in.

Usage:
  python build_deck.py <words.csv|words.xlsx|words.json> <output.html> [--deck "Tên bộ"] [--unit-size 20]

Input columns (header row, any order; names in Vietnamese/English/Chinese are recognised):
  Từ | Nghĩa | Phiên âm | Ngôn ngữ | Ví dụ      (only Từ and Nghĩa are required)
A JSON input may be a list of {"t","m","r","lang","ex"} objects.
The output is a single offline HTML file: open it in Chrome/Edge, no account needed.
"""
import argparse, csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "..", "assets", "so-tu-vung-a4-offline.html")
HEAD = {
    "t": r"^(từ|tu|từ vựng|tu vung|word|term|vocab|vocabulary|汉字|词语|单词|hanzi|chữ hán|từ mới)$",
    "m": r"^(nghĩa|nghia|meaning|tiếng việt|tieng viet|definition|dịch|vietnamese|nghĩa tiếng việt)$",
    "r": r"^(phiên âm|phien am|pinyin|ipa|pronunciation|phát âm|phat am|拼音|音标)$",
    "lang": r"^(ngôn ngữ|ngon ngu|lang|language)$",
    "ex": r"^(ví dụ|vi du|example|câu ví dụ|例句)$",
}
CJK = re.compile(r"[㐀-鿿豈-﫿]")

def read_rows(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        data = json.load(open(path, encoding="utf-8"))
        return None, data if isinstance(data, list) else data.get("words", [])
    if ext in (".xlsx", ".xlsm"):
        import openpyxl  # pip install openpyxl
        ws = openpyxl.load_workbook(path, read_only=True, data_only=True).active
        return [["" if c is None else str(c).strip() for c in row] for row in ws.iter_rows(values_only=True)], None
    with open(path, encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096); f.seek(0)
        delim = "\t" if "\t" in sample else ";" if sample.count(";") > sample.count(",") else ","
        return [[c.strip() for c in r] for r in csv.reader(f, delimiter=delim)], None

def to_words(aoa):
    aoa = [r for r in aoa if any(r)]
    if not aoa: return []
    head = [h.lower().strip() for h in aoa[0]]
    found = {}
    for i, h in enumerate(head):
        for k, pat in HEAD.items():
            if k not in found and re.match(pat, h, re.I): found[k] = i
    if "t" in found or "m" in found:
        cols, body = {"t": found.get("t", 0), "m": found.get("m", 1), "r": found.get("r", -1), "ex": found.get("ex", -1), "lang": found.get("lang", -1)}, aoa[1:]
    else:
        cols, body = {"t": 0, "m": 1, "r": 2, "ex": 3, "lang": -1}, aoa
    get = lambda r, k: r[cols[k]] if 0 <= cols[k] < len(r) else ""
    words = []
    for r in body:
        t, m = get(r, "t"), get(r, "m")
        if not t or not m: continue
        lang = get(r, "lang").lower()
        lang = "zh" if re.search(r"zh|trung|cn|中", lang) else "en" if re.search(r"en|anh", lang) else ("zh" if CJK.search(t) else "en")
        words.append({"t": t, "m": m, "r": get(r, "r"), "lang": lang, "ex": get(r, "ex")})
    return words

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--deck", default=None); ap.add_argument("--unit-size", type=int, default=20)
    a = ap.parse_args()
    aoa, words = read_rows(a.input)
    if words is None: words = to_words(aoa)
    words = [w for w in words if w.get("t") and w.get("m")]
    if not words: sys.exit("No words found: each row needs a word and a meaning.")
    deck = a.deck or os.path.splitext(os.path.basename(a.input))[0]
    payload = json.dumps({"deck": deck, "unitSize": max(5, min(60, a.unit_size)), "words": words}, ensure_ascii=False).replace("</", "<\\/")
    html = open(APP, encoding="utf-8").read()
    marker = '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/'
    assert marker in html, "app template changed: preload marker not found"
    html = html.replace(marker, "<script>window.A4_PRELOAD = " + payload + ";</script>\n" + marker, 1)
    html = re.sub(r"<title>.*?</title>", "<title>Sổ Từ Vựng A4 · " + deck.replace("<", "") + "</title>", html, count=1)
    open(a.output, "w", encoding="utf-8").write(html)
    zh = sum(w["lang"] == "zh" for w in words)
    print(f"OK: {a.output} · deck '{deck}' · {len(words)} words ({len(words)-zh} EN, {zh} ZH)")

if __name__ == "__main__":
    main()
