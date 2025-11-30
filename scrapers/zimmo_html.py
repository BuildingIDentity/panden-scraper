import requests
from bs4 import BeautifulSoup
from utils.db import save_property

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    )
}

def scrape_zimmo_html(postcode, type_mode):
    print(f"[Zimmo] Start {postcode} ({type_mode})")

    status = "1" if type_mode == "koop" else "2"
    url = f"https://www.zimmo.be/nl/zoeken/?location={postcode}&status={status}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
    except Exception as e:
        print(f"[Zimmo] Request fout: {e}")
        return

    if r.status_code != 200:
        print(f"[Zimmo] HTTP {r.status_code} → scraping mislukt")
        return

    soup = BeautifulSoup(r.text, "html.parser")
    cards = soup.select(".property-item--list")

    if not cards:
        print("[Zimmo] Geen resultaten of geblokkeerd.")
        return

    for card in cards:
        try:
            link_el = card.select_one("a.property-item_link")
            link = "https://www.zimmo.be" + link_el["href"] if link_el else None

            title_el = card.select_one(".property-item_title")
            title = title_el.get_text(strip=True) if title_el else "Geen titel"

            price_el = card.select_one(".property-item_price")
            price = price_el.get_text(strip=True) if price_el else "?"

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
                {"raw": card.text[:1500]},
            )

        except Exception as e:
            print("[Zimmo] Fout bij item:", e)

    print(f"[Zimmo] Klaar voor {postcode}.")
