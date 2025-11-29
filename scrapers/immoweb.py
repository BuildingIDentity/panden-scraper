import time
import random
import json
import requests
from bs4 import BeautifulSoup
from utils.db import save_property

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "nl-BE,nl;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Connection": "keep-alive",
}

def fetch_html(url):
    """HTML ophalen met retry zodat Immoweb Heroku niet blokkeert."""
    for attempt in range(3):
        try:
            time.sleep(random.uniform(0.4, 1.2))
            r = requests.get(url, headers=HEADERS, timeout=15)

            if r.status_code == 200:
                return r.text
            else:
                print(f"[Immoweb] status {r.status_code}")

        except Exception as e:
            print(f"[Immoweb] fout: {e}")

        print("[Immoweb] retry…")
        time.sleep(1 + attempt * 1.3)

    return None


def scrape_immoweb(postcode, type_mode):
    print(f"[Immoweb] Start {postcode} ({type_mode})")

    transaction = "SALE" if type_mode == "koop" else "RENT"

    url = (
        f"https://www.immoweb.be/nl/search"
        f"?type=HOUSE"
        f"&transaction={transaction}"
        f"&postalCode={postcode}"
    )

    html = fetch_html(url)
    if not html:
        print("[Immoweb] Geen HTML ontvangen")
        return

    soup = BeautifulSoup(html, "lxml")
    cards = soup.select("a.card--result")   # <-- de echte kaarten op Immoweb

    if not cards:
        print("[Immoweb] Geen kaarten gevonden — mogelijk blocking of andere layout")
        return

    print(f"[Immoweb] {len(cards)} items gevonden")

    for c in cards:
        link = "https://www.immoweb.be" + c.get("href")

        # ID
        extern_id = link.split("/")[-1]

        # Titel
        title_el = c.select_one(".card--result__title")
        titel = title_el.text.strip() if title_el else ""

        # Prijs
        price_el = c.select_one(".card--result__price")
        prijs = price_el.text.strip() if price_el else ""

        save_property(
            "immoweb",
            extern_id,
            type_mode,
            False,
            str(postcode),
            titel,
            prijs,
            link,
            {"raw": c.text}
        )

    print(f"[Immoweb] Klaar ({len(cards)} opgeslagen).")
