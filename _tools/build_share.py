"""Genera las vistas de solo lectura de cada cliente a partir de la página principal.

Uso (desde la raíz del repo):  python3 _tools/build_share.py

Cada vista incluye solo el marcado de su pestaña (sin Inicio, sin otras pestañas,
sin notas ni panel de sincronización) y lee sus datos de <código>/data.json,
que la página principal actualiza al guardar.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "3ocz9gy6iwl7" / "index.html"
SHARES = {"rocket": "cbqupfrchc", "shopify": "lm7l8rjbdi"}
NAMES = {"rocket": "Rocket Digital", "shopify": "Shopify"}


def cut_block(s: str, start_pat: str, tag: str) -> str:
    """Remove the element that starts at start_pat, matching nested <tag> depth."""
    i = s.find(start_pat)
    if i < 0:
        return s
    depth = 0
    for m in re.finditer(rf"<{tag}\b|</{tag}>", s[i:]):
        depth += 1 if m.group(0).startswith(f"<{tag}") else -1
        if depth == 0:
            j = i + m.end()
            k = s.rfind("\n", 0, i)
            return s[:k] + s[j:]
    raise ValueError(f"unclosed {start_pat}")


def build(client: str, code: str) -> str:
    s = MAIN.read_text(encoding="utf-8")
    s = cut_block(s, '<nav class="tabs"', "nav")
    for other in ["home", *[c for c in SHARES if c != client]]:
        s = cut_block(s, f'<section class="panel" id="p-{other}"', "section")
    s = cut_block(s, '<div class="syncpanel"', "div")
    s = re.sub(r'<button type="button" class="syncbtn"[^>]*>.*?</button>', "", s)
    s = s.replace(f'id="p-{client}" role="tabpanel" aria-labelledby="tab-{client}" data-client="{client}" hidden',
                  f'id="p-{client}" data-client="{client}"')
    s = re.sub(r'^<script type="application/json" id="state">.*?</script>$',
               '<script type="application/json" id="state">{}</script>', s, count=1, flags=re.S | re.M)
    s = re.sub(r"var CL = \{.*?\};", lambda m: "var CL = {" + re.search(client + r":\{[^}]*\}", m.group(0)).group(0) + "};", s)
    s = s.replace("var SHARES = {rocket: 'cbqupfrchc', shopify: 'lm7l8rjbdi'}", "var SHARES = {}")
    s = s.replace("window.ARMI_DATA || 'd/3unwb8j9lfbwts0b.json'", "window.ARMI_DATA")
    s = re.sub(r"<title>.*?</title>", f"<title>{NAMES[client]} · Agenda</title>", s)
    s = s.replace('<script id="app">',
                  f'<script>window.ARMI_VIEW = "{client}"; window.ARMI_DATA = "{code}/data.json";</script>\n<script id="app">', 1)
    # Other clients' codes and task lists must not appear (Rocket works with Shopify, so the name itself can)
    for other, oc in SHARES.items():
        if other != client:
            assert oc not in s and "Bootcamp" not in s if other == "shopify" else oc not in s, f"{other} leaked into {client}"
    assert "3unwb8j9lfbwts0b" not in s and "3ocz9gy6iwl7" not in s
    return s


def build_template() -> str:
    """Generic read-only viewer for clients created from the page (no client data inside)."""
    s = MAIN.read_text(encoding="utf-8")
    s = cut_block(s, '<nav class="tabs"', "nav")
    for other in ["home", *SHARES]:
        s = cut_block(s, f'<section class="panel" id="p-{other}"', "section")
    s = cut_block(s, '<div class="syncpanel"', "div")
    s = re.sub(r'<button type="button" class="syncbtn"[^>]*>.*?</button>', "", s)
    s = re.sub(r'^<script type="application/json" id="state">.*?</script>$',
               '<script type="application/json" id="state">{}</script>', s, count=1, flags=re.S | re.M)
    s = re.sub(r"var CL = \{.*?\};", "var CL = {};", s, count=1)
    s = s.replace("var SHARES = {rocket: 'cbqupfrchc', shopify: 'lm7l8rjbdi'}", "var SHARES = {}")
    s = s.replace("window.ARMI_DATA || 'd/3unwb8j9lfbwts0b.json'", "window.ARMI_DATA")
    s = re.sub(r"<title>.*?</title>", "<title>Agenda</title>", s)
    s = s.replace('<script id="app">', '<script>/*ARMI_VIEW_INIT*/</script>\n<script id="app">', 1)
    for code in [*SHARES.values(), "3unwb8j9lfbwts0b", "3ocz9gy6iwl7"]:
        assert code not in s, code
    for word in ["Rocket Digital", "Bootcamp", "Critical Quarter"]:
        assert word not in s, word
    return s


if __name__ == "__main__":
    for client, code in SHARES.items():
        out = ROOT / code / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(build(client, code), encoding="utf-8")
        print("ok", client, "->", out.relative_to(ROOT))
    (ROOT / "_tools" / "viewer.html").write_text(build_template(), encoding="utf-8")
    print("ok template -> _tools/viewer.html")
