import requests
from bs4 import BeautifulSoup
import time
import random
from utils.db import save_property

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "nl-NL,nl;q=0.9",
    "Referer": "https://www.zimmo.be/nl/",
    "Connection": "keep-alive",
}

def scrape_zimmo(postcode, type_mode):
    print(f"[Zimmo] Start {postcode} ({type_mode})")

    status = "1" if type_mode == "koop" else "2"
    url = f"https://www.zimmo.be/nl/zoeken/?status={status}&location={postcode}"

    try:
        time.sleep(random.uniform(1.2, 2.0))
        r = requests.get(url, headers=HEADERS, timeout=20)
    except Exception as e:
        print(f"[Zimmo] Request error: {e}")
        return

    if r.status_code != 200:
        print(f"[Zimmo] Fout {r.status_code}")
        return

    soup = BeautifulSoup(r.text, "lxml")

    items = soup.select("article.search-results__item")
    print(f"[Zimmo] gevonden: {len(items)} items")

    if len(items) == 0:
        print("[Zimmo] Geen resultaten gevonden (selector?)")
        return

    for item in items:
        link_tag = item.select_one("a")
        title_tag = item.select_one("h2.search-results__title")
        price_tag = item.select_one("div.search-results__price")

        link = "https://www.zimmo.be" + link_tag.get("href") if link_tag else None
        title = title_tag.get_text(strip=True) if title_tag else ""
        price = price_tag.get_text(strip=True) if price_tag else ""

        extern_id = link.split("/")[-2] if link else None

        save_property(
            "zimmo",
            extern_id,
            type_mode,
            False,
            str(postcode),
            title,
            price,
            link,
            {"raw": item.get_text(strip=True)}
        )

    print(f"[Zimmo] Klaar.")
