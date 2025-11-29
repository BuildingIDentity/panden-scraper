import requests
from bs4 import BeautifulSoup
import json
from utils.db import save_property

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_immoscoop(postcode, type_mode):
    print(f"[Immoscoop] Start {postcode} ({type_mode})")

    url = (
        f"https://www.immoscoop.be/nl/te-koop?location={postcode}"
        if type_mode == "koop"
        else f"https://www.immoscoop.be/nl/te-huur?location={postcode}"
    )

    r = requests.get(url, headers=HEADERS, timeout=20)
    if r.status_code != 200:
        print(f"[Immoscoop] Fout {r.status_code}")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select("a.immo-property-card")
    if not cards:
        print("[Immoscoop] Geen resultaten")
        return

    total = 0

    for c in cards:
        link = c.get("href")
        if link.startswith("/"):
            link = "https://www.immoscoop.be" + link

        titel = c.select_one(".title")
        titel = titel.text.strip() if titel else ""

        prijs = c.select_one(".price")
        prijs = prijs.text.strip() if prijs else ""

        extern_id = link.split("/")[-1].split("?")[0]

        save_property(
            "immoscoop",
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

    print(f"[Immoscoop] Klaar. {total} panden opgeslagen.")
