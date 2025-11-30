import requests
from bs4 import BeautifulSoup
from utils.db import save_property

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/120.0.0.0 Safari/537.36"
    )
}

def scrape_immovlan(postcode, type_mode):
    print(f"[Immovlan] Start {postcode} ({type_mode})")

    # correct domein + correcte URL-structuur
    if type_mode == "koop":
        url = f"https://www.immovlan.be/nl/zoeken/huis/te-koop?loc={postcode}"
    else:
        url = f"https://www.immovlan.be/nl/zoeken/huis/te-huur?loc={postcode}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
    except Exception as e:
        print(f"[Immovlan] Request error: {e}")
        return

    if r.status_code != 200:
        print(f"[Immovlan] Fout {r.status_code} bij {url}")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select(".search-results__item")

    if not cards:
        print(f"[Immovlan] Geen resultaten gevonden.")
        return

    for card in cards:
        try:
            link_el = card.select_one("a")
            link = link_el["href"] if link_el else None
            if link and link.startswith("/"):
                link = "https://www.immovlan.be" + link

            extern_id = link.split("/")[-1] if link else None

            title_el = card.select_one("h2")
            title = title_el.get_text(strip=True) if title_el else "Geen titel"

            price_el = card.select_one(".search-results__price")
            price = price_el.get_text(strip=True) if price_el else "?"

            save_property(
                "immovlan",
                extern_id,
                type_mode,
                False,
                str(postcode),
                title,
                price,
                link,
                {"raw": card.text[:2000]},
            )
        except Exception as e:
            print(f"[Immovlan] Fout bij item: {e}")

    print(f"[Immovlan] Klaar voor {postcode}.")
