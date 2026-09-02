#!/usr/bin/env python3
"""
Scrapea las últimas noticias de un tag de canal26.com y las guarda en
news.json para que el zócalo del countdown las muestre.

Estrategia, en orden:
  1. Buscar un feed RSS/Atom autodiscoverable (<link rel="alternate">) o
     probar rutas típicas de feed (/feed/, ?feed=rss2, etc.) — es la fuente
     más estable si existe.
  2. Si no hay feed, hacer scraping genérico del HTML: buscar enlaces de
     artículo (fuera del header/nav) con texto largo, tal como aparecen
     los titulares en la página de tag.

Corre desde GitHub Actions (con salida a internet completa), no desde
este sandbox. Si falla, deja el news.json existente intacto para no
romper el zócalo con una lista vacía.
"""
import json
import re
import sys
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

TAG_URL = "https://www.canal26.com/tag/papa-leon-xiv/"
OUTPUT_PATH = "news.json"
MAX_ITEMS = 10
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

NAV_TEXT_BLOCKLIST = {
    "lo último", "internacionales", "policiales", "política", "economía",
    "clima", "planeta", "turismo", "newsletters", "nuevo", "canal 26 en vivo",
    "en vivo",
}


def fetch(url, **kwargs):
    resp = requests.get(url, headers=HEADERS, timeout=20, **kwargs)
    resp.raise_for_status()
    return resp


def try_feed_from_page(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find("link", attrs={"rel": "alternate", "type": re.compile("rss|atom")})
    if link and link.get("href"):
        return urljoin(base_url, link["href"])
    return None


def try_common_feed_paths(base_url):
    candidates = [
        urljoin(base_url, "feed/"),
        urljoin(base_url, "feed/rss2/"),
        base_url.rstrip("/") + "/feed",
    ]
    for url in candidates:
        try:
            resp = fetch(url)
            if "xml" in resp.headers.get("Content-Type", "") or resp.text.lstrip().startswith("<?xml"):
                return url
        except requests.RequestException:
            continue
    return None


def parse_feed(feed_url):
    import feedparser

    parsed = feedparser.parse(feed_url)
    items = []
    for entry in parsed.entries[:MAX_ITEMS]:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if title:
            items.append({"title": title, "url": link})
    return items


def scrape_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    # Sacar header/nav/footer para no levantar links de navegación.
    for tag_name in ("header", "nav", "footer"):
        for el in soup.find_all(tag_name):
            el.decompose()

    seen_urls = set()
    items = []
    domain = urlparse(base_url).netloc

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        if not text or len(text) < 25:
            continue
        if text.lower() in NAV_TEXT_BLOCKLIST:
            continue
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc != domain:
            continue
        if full_url in seen_urls:
            continue
        # Los artículos de este tipo de sitio suelen tener slug numérico o
        # de fecha en la URL; filtra links de navegación tipo /tag/, /autor/.
        path = urlparse(full_url).path
        if path.count("/") < 2:
            continue
        seen_urls.add(full_url)
        items.append({"title": text, "url": full_url})
        if len(items) >= MAX_ITEMS:
            break

    return items


def main():
    try:
        page = fetch(TAG_URL)
    except requests.RequestException as exc:
        print(f"ERROR: no se pudo bajar {TAG_URL}: {exc}", file=sys.stderr)
        sys.exit(1)

    feed_url = try_feed_from_page(page.text, TAG_URL) or try_common_feed_paths(TAG_URL)
    items = []

    if feed_url:
        print(f"Feed encontrado: {feed_url}")
        try:
            items = parse_feed(feed_url)
        except Exception as exc:
            print(f"WARN: fallo parseando feed ({exc}), sigo con scraping HTML", file=sys.stderr)

    if not items:
        print("Sin feed usable, scrapeando HTML directamente")
        items = scrape_html(page.text, TAG_URL)

    print(f"Encontradas {len(items)} noticias:")
    for it in items:
        print(f"  - {it['title']}")

    if not items:
        print("ERROR: no se encontró ninguna noticia, no se sobreescribe news.json", file=sys.stderr)
        sys.exit(1)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
