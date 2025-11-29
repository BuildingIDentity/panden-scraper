from utils.fetcher import fetch
from utils.db import get_connection
from utils.filters import is_particulier
from bs4 import BeautifulSoup
import json

def scrape_zimmo(postcode, type_mode):
    # type_mode = "koop" of "huur"
    if type_mode == "koop":
        base = f"https://www.zimmo.be/nl/zoeken/?location={postcode}&status=1"
    else:
        base = f"https://www.zimmo.be/nl/zoeken/?location={postcode}&status=2"

    html = fetch(base)
    if not html:
        return

    soup = BeautifulSoup(html, "lxml")
    items = soup.select(".property-item")

    conn = get_connection()
    cur = conn.cursor()

    for x in items:
        link = x.get("href")
        titel = x.select_one(".property-item--title")
        titel = titel.text.strip() if titel else ""

        prijs = x.select_one(".price")
        prijs = prijs.text.strip() if prijs else ""

        extern_id = None
        if link:
            extern_id = link.split("/")[-2]

        particulier = is_particulier(titel, "", x.text)

        cur.execute("""
            INSERT INTO panden (bron, extern_id, type, particulier, postcode, titel, prijs, link, data)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (bron, extern_id)
            DO UPDATE SET updated_at = NOW();
        """, ("zimmo", extern_id, type_mode, particulier, postcode, titel, prijs, link, json.dumps({"raw": x.text})))

    conn.commit()
    conn.close()

