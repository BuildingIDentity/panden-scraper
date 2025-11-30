import requests
from utils.db import save_property

def scrape_zimmo(postcode, type_mode):
    print(f"[Zimmo] Start {postcode} ({type_mode})")

    # type 1 = koop, type 2 = huur
    status = "1" if type_mode == "koop" else "2"

    url = (
        f"https://www.zimmo.be/nl/zoeken/"
        f"?location={postcode}&status={status}&result=JSON"
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 403:
            print("[Zimmo] 403: Zimmo blokkeert je request")
            print("→ Dit lossen we op met cookies, geen paniek.")
            return

        data = resp.json()
    except Exception as e:
        print(f"[Zimmo] Fout: {e}")
        return

    items = data.get("items", [])
    if not items:
        print("[Zimmo] Geen items gevonden.")
        return

    for item in items:
        try:
            save_property(
                "zimmo",
                item.get("id"),
                type_mode,
                False,
                str(postcode),
                item.get("title", "Zonder titel"),
                item.get("price", "Onbekend"),
                item.get("url"),
                item,
            )
        except Exception as e:
            print("[Zimmo] Item fout:", e)

    print(f"[Zimmo] Klaar ({len(items)} panden)")
