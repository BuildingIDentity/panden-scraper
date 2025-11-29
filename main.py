import json
from utils.db import init_tables
from scrapers.immoweb import scrape_immoweb
from scrapers.zimmo import scrape_zimmo
from scrapers.immoscoop import scrape_immoscoop
from scrapers.tweedehands import scrape_tweedehands
from scrapers.immovlam import scrape_immovlam

def load_postcodes():
    with open("config/postcodes.json", "r") as f:
        return json.load(f)

def main():
        print("Initialiseren tabellen...")
        init_tables()

        postcodes = load_postcodes()

        for pc in postcodes[:2]:
            print(f"Scrapen immoweb {pc}")
            scrape_immoweb(pc, "koop")
            scrape_immoweb(pc, "huur")

            print(f"Scrapen zimmo {pc}")
            scrape_zimmo(pc, "koop")
            scrape_zimmo(pc, "huur")

            print(f"Scrapen immoscoop {pc}")
            scrape_immoscoop(pc, "koop")
            scrape_immoscoop(pc, "huur")

            print(f"Scrapen tweedehands {pc}")
            scrape_tweedehands(pc, "koop")
            scrape_tweedehands(pc, "huur")

            print(f"Scrapen immovlam {pc}")
            scrape_immovlam(pc, "koop")
            scrape_immovlam(pc, "huur")

        print("Klaar.")

if __name__ == "__main__":
    main()
