from utils.fetcher import fetch
from utils.db import get_connection
from utils.filters import is_particulier
from bs4 import BeautifulSoup
import json

def scrape_immoweb(postcode):
    url = f"https://www.immoweb.be/nl/zoeken/huis/te-koop/postcode-{postcode}"
    html = fetch(url)
    if not html:
        return
    
    soup = BeautifulSoup(html, "lxml")
    results = soup.select("a.card--result")
    
    conn = get_connection()
    cur = conn.cursor()

    for item in results:
        link = item.get("href")
        titel = item.select_one(".result-title")
        titel = titel.text.strip() if titel else ""

        prijs = item.select_one(".result-price")
        prijs = prijs.text.strip() if prijs else ""

        extern_id = None
        if link and "/id/" in link:
            extern_id = link.split("/id/")[1][:10]

        particulier = is_particulier(titel, "", item.text)

        cur.execute("""
            INSERT INTO panden (bron, extern_id, type, particulier, postcode, titel, prijs, link, data)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (bron, extern_id)
            DO UPDATE SET updated_at = NOW();
        """, ("immoweb", extern_id, "koop", particulier, postcode, titel, prijs, link, json.dumps({"raw": item.text})))

    conn.commit()
    conn.close()

