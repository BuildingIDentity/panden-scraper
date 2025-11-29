import requests
from utils.db import save_property
import json

BASE_URL = "https://api.immoweb.be/search/search-results"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def scrape_immoweb(postcode, type_mode):
    print(f"[Immoweb] Start {postcode} ({type_mode})")

    transaction = "FOR_SALE" if type_mode == "koop" else "FOR_RENT"
    page = 1
    total = 0

    while True:
        url = (
            f"{BASE_URL}?postalCode={postcode}"
            f"&transactionTypes={transaction}"
            f"&propertyTypes=HOUSE&page={page}"
        )

        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"[Immoweb] Fout {r.status_code}")
            break

        data = r.json()
        results = data.get("results", [])
        if not results:
            print(f"[Immoweb] Geen resultaten meer op pagina {page}")
            break

        for item in results:
            extern_id = str(item.get("id"))
            titel = item.get("title", "")
            prijs = item.get("price", {}).get("mainValue", "")
            link = f"https://www.immoweb.be/nl/zoekertje/{extern_id}"

            save_property(
                "immoweb",
                extern_id,
                type_mode,
                False,
                str(postcode),
                titel,
                prijs,
                link,
                item
            )
            total += 1

        page += 1

    print(f"[Immoweb] Klaar. {total} panden opgeslagen.")
