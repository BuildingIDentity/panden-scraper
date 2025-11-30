import requests
from utils.db import save_property

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Cookie": "cf_clearance=6sY_0Q3f53prpAr_K_svMVqWbKuTlIQaVZdSpXS.IHs-1764462956-1.2.1.1-bW5x7tbKia0ajAwQW9HuWJ0h9pisMJcanZCDqznZa7YFBEqrG_XfTZsGukKv8vTl3EnwA0iSW9jwPyw7_SV9OvYrqnxRkUIWaQ5juMhloln8NBp6iZ3baKNU82UGWzffcc36C9b9kq6ssWAiJHLWgpuAqJofr0jJAfBUrxTicLtw4eOKlxKt9qaMsjcJC7Eyh8F5KRQ3K9jYssat6iVUKD_cGH7brfRd42oHkDu3.ts"
}

def scrape_zimmo(postcode, type_mode):
    print(f"[Zimmo] Start {postcode} ({type_mode})")

    status = "1" if type_mode == "koop" else "2"
    url = f"https://www.zimmo.be/nl/zoeken/?location={postcode}&status={status}&result=JSON"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)

        if resp.status_code == 403:
            print("[Zimmo] 403 → Cookie verlopen. Nieuwe nodig.")
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
                item.get("title") or "Zonder titel",
                item.get("price") or "Onbekend",
                item.get("url"),
                item,
            )
        except Exception as e:
            print("[Zimmo] Item fout:", e)

    print(f"[Zimmo] Klaar ({len(items)} panden)")
