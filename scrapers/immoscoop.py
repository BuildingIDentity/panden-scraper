from utils.fetcher import fetch
from utils.db import get_connection
from utils.filters import is_particulier
from bs4 import BeautifulSoup
import json

def scrape_immoscoop(postcode, type_mode):
    if type_mode == "koop":
        url = f"https://www.immoscoop.be/te-koop?location={postcode}"
    else:
        url = f"https://www.immoscoop.be/te-huur?location={postcode}"

    html = fetch(url)
    if not html:
        return

    soup = BeautifulSoup(html, "lxml")
    cards = soup.select(".property-card")

    conn = get_connection()
    cur = conn.cursor()

    for c in cards:
        link = c.get("href")
        titel = c.select_one(".property-card__title")
        titel = titel.text.strip() if titel else ""

        prijs = c.select_one(".property-card__price")
        prijs = prijs.text.strip() if prijs else ""

        extern_id = link.split("/")[-1] if link else None

        particulier = is_particulier(titel, "", c.text)

        cur.execute("""
            INSERT INTO panden (bron, extern_id, type, particulier, postcode, titel, prijs, link, data)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (bron, extern_id)
            DO UPDATE SET updated_at = NOW();
        """, ("immoscoop", extern_id, type_mode, particulier, postcode, titel, prijs, link, json.dumps({"raw": c.text})))

    conn.commit()
    conn.close()

