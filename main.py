import json
from utils.db import init_tables
from scrapers.immoweb import scrape_immoweb

def load_postcodes():
    with open("config/postcodes.json", "r") as f:
        return json.load(f)

def main():
    print("Initialiseren tabellen...")
    init_tables()
    
    postcodes = load_postcodes()

    # Test: eerst 1 postcode
    for pc in postcodes[:1]:
        print(f"Scrapen immoweb {pc}")
        scrape_immoweb(pc)

    print("Klaar.")

if __name__ == "__main__":
    main()

