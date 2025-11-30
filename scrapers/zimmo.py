import requests
from utils.db import save_property

def scrape_zimmo(postcode, type_mode):
    print(f"[Zimmo] Start {postcode} ({type_mode})")

    type_filter = "1" if type_mode == "koop" else "2"

    url = (
        f"https://www.zimmo.be/nl/zoeken/?"
        f"location={postcode}&status={type_filter}&result=JSON"
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        data = r.json()
    except Exception as e:
        print(f"[Zimmo] Fout: {e}")
        return

    results = data.get("items", [])

    if not results:
        print("[Zimmo] Geen items gevonden.")
        return

    for item in results:
        try:
            extern_id = item["id"]
            title = item.get("title", "Zonder titel")
            price = item.get("price", "Onbekend")
            link = item["url"]

            save_property(
                "zimmo",
                extern_id,
                type_mode,
                False,
                str(postcode),
                title,
                price,
                link,
                item
            )
        except Exception as e:
            print(f"[Zimmo] Error item: {e}")

    print(f"[Zimmo] Klaar ({len(results)} panden).")
