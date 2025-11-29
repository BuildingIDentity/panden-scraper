import requests
from bs4 import BeautifulSoup
from utils.db import save_property

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_immovlam(postcode, type_mode):
    print(f"[Immovlam] Start {postcode} ({type_mode})")

    transaction = "SALE" if type_mode == "koop" else "RENT"

    url = (
        "https://www.immovlam.be/nl/zoeken"
        f"?type=HOUSE&transaction={transaction}&postalCode={postcode}"
    )

    r = requests.get(url, headers=HEADERS, timeout=20)
    if r.status_code != 200:
        print(f"[Immovlam] Fout {r.status_code}")
        return

    soup = BeautifulSoup(r.text, "html.parser")
    cards = soup.select(".search-result__item")

    total = 0

    for c in cards:
        title_el = c.select_one(".search-result__title")
        titel = title_el.text.strip() if title_el else ""

        price_el = c.select_one(".search-result__price")
        prijs = price_el.text.strip() if price_el else ""

        link_el = c.select_one("a")
        link = "https://www.immovlam.be" + link_el["href"]

        extern_id = link.split("/")[-1]

        save_property(
            "immovlam",
            extern_id,
            type_mode,
            False,
            str(postcode),
            titel,
            prijs,
            link,
            {"raw": c.text}
        )
        total += 1

    print(f"[Immovlam] Klaar. {total} panden opgeslagen.")
