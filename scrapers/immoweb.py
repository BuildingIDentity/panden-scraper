from utils.fetcher import fetch
from utils.db import get_connection
from bs4 import BeautifulSoup
import json

def scrape_immoweb(postcode, type_mode):
    if type_mode == "koop":
        url = f"https://www.immoweb.be/nl/search?type=HOUSE&transaction=SALE&postalCode={postcode}"
    else:
        url = f"https://www.immoweb.be/nl/search?type=HOUSE&transaction=RENT&postalCode={postcode}"

    html = fetch(url)
    if not html:
        print("Geen HTML ontvangen van Immoweb")
        return

    soup = BeautifulSoup(html, "lxml")
    items = soup.select("a.card__title")

    conn = get_connection()
    cur = conn.cursor()

    for item in items:
        link = "https://www.immoweb.be" + item.get("href")
        titel = item.text.strip()

        extern_id = link.split("/")[-1]

        cur.execute("""
            INSERT INTO panden (bron, extern_id, type, particulier, postcode, titel, link, data)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (bron, extern_id)
            DO UPDATE SET updated_at = NOW();
        """, ("immoweb", extern_id, type_mode, False, postcode, titel, link, json.dumps({"raw": titel})))

    conn.commit()
    conn.close()
    print(f"Immoweb klaar voor {postcode}")
