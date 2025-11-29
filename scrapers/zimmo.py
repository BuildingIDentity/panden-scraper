import requests
from bs4 import BeautifulSoup
import json
from utils.db import save_property

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_zimmo(postcode, type_mode):
    print(f"[Zimmo] Start {postcode} ({type_mode})")

    status = "1" if type_mode == "koop" else "2"
    url = f"https://www.zimmo.be/nl/zoeken/?location={postcode}&status={status}"

    r = requests.get(url, headers=HEADERS, timeout=20)
    if r.status_code != 200:
        print(f"[Zimmo] Fout {r.status_code}")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # JSON staat in window.__SSR_STATE__
    script = soup.find("script", string=lambda s: s and "window.__SSR_STATE__" in s)
    if not script:
        print("[Zimmo] Geen JSON gevonden")
        return

    json_text = script.string.split("window.__SSR_STATE__ =")[-1].strip()
    json_text = json_text[:-1] if json_text.endswith(";") else json_text

    data = json.loads(json_text)

    properties = data.get("listing", {}).get("results", [])
    total = 0

    for p in properties:
        extern_id = str(p.get("id"))
        titel = p.get("title", "")
        prijs = p.get("price", "")
        link = p.get("url", "")

        save_property(
            "zimmo",
            extern_id,
            type_mode,
            p.get("isPrivate", False),
            str(postcode),
            titel,
            prijs,
            link,
            p
        )
        total += 1

    print(f"[Zimmo] Klaar. {total} panden opgeslagen.")
