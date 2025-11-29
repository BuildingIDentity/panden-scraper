import requests
from bs4 import BeautifulSoup
from utils.db import save_property   # zelfde structuur als andere scrapers
import time
import random

BASE_URL = "https://www.2dehands.be/l/huizen-en-vastgoed/huis-te-koop/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "nl-BE,nl;q=0.9,en;q=0.8",
}


def fetch_html(url):
    """Doet request met headers + random delay om 403 te vermijden."""
    try:
        time.sleep(random.uniform(0.5, 1.4))
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            return r.text
        else:
            print(f"[Tweedehands] Fout {r.status_code} bij {url}")
            return None
    except Exception as e:
        print(f"[Tweedehands] Request error: {e}")
        return None


def parse_listing(card):
    """Zet een HTML zoekresultaat om naar een dict."""
    try:
        title = card.select_one("h2").get_text(strip=True)
        price_el = card.select_one(".Listing-price")
        price = price_el.get_text(strip=True) if price_el else "Onbekend"

        link_el = card.select_one("a")
        link = "https://www.2dehands.be" + link_el["href"]

        location_el = card.select_one(".Listing-location")
        location = location_el.get_text(strip=True) if location_el else "Onbekend"

        return {
            "title": title,
            "price": price,
            "location": location,
            "url": link
        }
    except:
        return None


def scrape_page(pc, page):
    """Scrap één pagina van 2dehands zoekresultaten."""
    url = f"{BASE_URL}?postcode={pc}&page={page}"

    html = fetch_html(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    cards = soup.select("article.Listing")

    results = []
    for c in cards:
        info = parse_listing(c)
        if info:
            results.append(info)

    return results


def scrape_tweedehands(pc, type_mode):
    """
    type_mode wordt genegeerd (Tweedehands heeft geen koop/huur scheiding),
    maar we volgen jouw functie-structuur.
    """
    print(f"[Tweedehands] Scrapen postcode {pc} ({type_mode})")

    all_results = []
    
    # max 3 pagina's om blokkering te voorkomen
    for page in range(1, 4):
        print(f"[Tweedehands] Pagina {page}...")
        page_results = scrape_page(pc, page)
        if not page_results:
            break

        # opslaan zoals jouw andere scrapers
        for item in page_results:
            save_property(
                platform="tweedehands",
                postcode=pc,
                type_mode=type_mode,
                title=item["title"],
                price=item["price"],
                location=item["location"],
                url=item["url"]
            )

        all_results.extend(page_results)

    print(f"[Tweedehands] {len(all_results)} resultaten gevonden.")
    return all_results
