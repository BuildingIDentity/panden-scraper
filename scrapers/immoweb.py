from utils.fetcher import fetch
from utils.db import get_connection
from bs4 import BeautifulSoup
import json

def scrape_immoweb(postcode, type_mode):
    if type_mode == "koop":
        url = f"https://www.immoweb.be/nl/search?type=HOUSE&transaction=SALE&postalCode={postcode}"
    else:
        url = f"https://www.immoweb.be/nl/search?type=HOUSE&transaction=RENT&postalCode={postcode}"

    print(f"[Immoweb] URL: {url}")

    html = fetch(url)
    if not html:
        print("[Immoweb] Geen HTML ontvangen (fetch = None)")
        return

    print("[Immoweb] HTML ontvangen")

    soup = BeautifulSoup(html, "lxml")
    items = soup.select("a.card__title")

    print(f"[Immoweb] Gevonden items: {len(items)}")

    if len(items) == 0:
        print("[Immoweb] Waarschijnlijk nog steeds geblokkeerd of andere selector")
        return

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
    print(f"[Immoweb] Klaar voor {postcode} ({type_mode})")
