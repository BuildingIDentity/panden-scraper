from utils.fetcher import fetch
from utils.db import get_connection
from utils.filters import is_particulier
from bs4 import BeautifulSoup
import json
import requests

def scrape_immoscoop(postcode, type_mode):
    if type_mode == "koop":
        url = f"https://www.immoscoop.be/nl/te-koop?location={postcode}"
    else:
        url = f"https://www.immoscoop.be/nl/te-huur?location={postcode}"

    # Hard headers – Heroku heeft dit nodig
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "nl-NL,nl;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
    except Exception as e:
        print(f"[Immoscoop] Request error: {e}")
        return

    if r.status_code != 200:
        print(f"[Immoscoop] Fout {r.status_code} bij URL {url}")
        return

    html = r.text
    soup = BeautifulSoup(html, "lxml")

    cards = soup.select("a.immo-property-card")
    if not cards:
        print(f"[Immoscoop] Geen resultaten gevonden voor {postcode} ({type_mode})")
        return

    conn = get_connection()
    cur = conn.cursor()

    for c in cards:
        link = c.get("href")
        if link and link.startswith("/"):
            link = "https://www.immoscoop.be" + link

        titel_el = c.select_one(".title")
        titel = titel_el.get_text(strip=True) if titel_el else ""

        prijs_el = c.select_one(".price")
        prijs = prijs_el.get_text(strip=True) if prijs_el else ""

        extern_id = link.split("/")[-1].split("?")[0] if link else None

        particulier = is_particulier(titel, "", c.text)

        cur.execute("""
            INSERT INTO panden (bron, extern_id, type, particulier, postcode, titel, prijs, link, data)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (bron, extern_id)
            DO UPDATE SET updated_at = NOW();
        """, (
            "immoscoop", extern_id, type_mode, particulier,
            postcode, titel, prijs, link,
            json.dumps({"raw": c.text})
        ))

    conn.commit()
    conn.close()

    print(f"[Immoscoop] {len(cards)} panden opgeslagen voor {postcode} ({type_mode})")
