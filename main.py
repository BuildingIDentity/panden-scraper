import json
from utils.db import init_tables
from scrapers.zimmo import scrape_zimmo

def load_postcodes():
    with open("config/postcodes.json", "r") as f:
        return json.load(f)

def main():
    print("Initialiseren tabellen...")
    init_tables()

    postcodes = load_postcodes()

    for pc in postcodes[:1]:   # enkel 1 postcode om te testen
        print(f"Scrapen zimmo {pc}")
        scrape_zimmo(pc, "koop")
        scrape_zimmo(pc, "huur")

    print("Klaar.")

# Heroku gebruikt gunicorn, dus lokaal runnen mag wel:
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
