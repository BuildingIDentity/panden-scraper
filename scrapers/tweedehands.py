import requests
from bs4 import BeautifulSoup
import time
import random
from utils.db import save_property

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "nl-BE"
}

def scrape_tweedehands(postcode, type_mode):
    print(f"[2dehands] Start {postcode}")

    base = f"https://www.2dehands.be/l/huizen-en-vastgoed/?postcode={postcode}"
    total = 0

    for page in range(1, 4):
        url = f"{base}&page={page}"

        time.sleep(random.uniform(0.4, 1.2))
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            break

        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select("article.Listing")

        if not cards:
            break

        for c in cards:
            title_el = c.select_one("h2")
            title = title_el.text.strip() if title_el else ""

            price_el = c.select_one(".Listing-price")
            prijs = price_el.text.strip() if price_el else ""

            link_el = c.select_one("a")
            link = "https://www.2dehands.be" + link_el["href"]

            extern_id = link.split("/")[-1].split("-")[0]

            save_property(
                "tweedehands",
                extern_id,
                type_mode,
                False,
                str(postcode),
                title,
                prijs,
                link,
                {"raw": c.text}
            )
            total += 1

    print(f"[2dehands] Klaar. {total} panden opgeslagen.")
