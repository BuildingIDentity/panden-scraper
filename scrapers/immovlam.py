import requests
from bs4 import BeautifulSoup
from utils.db import save_property

BASE_URL = "https://www.immovlam.be/nl/zoeken"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def scrape_immovlam(postcode, type_mode):
    """
    Scraper voor ImmoVlam.
    type_mode = 'koop' of 'huur'
    """

    print(f"[ImmoVlam] Start scraping {postcode} ({type_mode})...")

    # Bouw correcte URL
    if type_mode == "koop":
        search_type = "te-koop"
    else:
        search_type = "te-huur"

    url = f"{BASE_URL}/huis/{search_type}/postcode-{postcode}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"[ImmoVlam] Fout {response.status_code} bij {url}")
            return
    except Exception as e:
        print(f"[ImmoVlam] Request error: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Kaartjes staan meestal in <article> of <div class="property-card">
    cards = soup.select("article, .property-card, .result-item")

    if not cards:
        print(f"[ImmoVlam] Geen resultaten gevonden voor {postcode} ({type_mode}).")
        return

    for card in cards:
        try:
            # Titel
            title_tag = card.select_one("h2, h3, .title")
            title = title_tag.get_text(strip=True) if title_tag else "Geen titel"

            # Link
            link_tag = card.select_one("a")
            link = "https://www.immovlam.be" + link_tag["href"] if link_tag and link_tag.get("href") else None

            # ID afleiden
            extern_id = None
            if link and "/detail/" in link:
                extern_id = link.split("/detail/")[-1].split("/")[0]

            # Prijs
            price_tag = card.select_one(".price, .prijs, .amount")
            price = price_tag.get_text(strip=True) if price_tag else "Onbekend"

            # Data opslaan
            save_property(
                bron="immovlam",
                extern_id=extern_id or link,  # fallback
                type=type_mode,
                particulier=False,
                postcode=str(postcode),
                titel=title,
                prijs=price,
                link=link,
                data={
                    "scraped_from": "Immovlam",
                    "raw_html": str(card)[:5000]  # beperkte backup
                }
            )

        except Exception as e:
            print(f"[ImmoVlam] Fout bij verwerken kaartje: {e}")
            continue

    print(f"[ImmoVlam] Klaar voor {postcode} ({type_mode}).")

