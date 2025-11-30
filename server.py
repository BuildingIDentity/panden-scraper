from flask import Flask, request, jsonify
from scrapers.zimmo_html import scrape_zimmo_html

app = Flask(__name__)

@app.get("/")
def home():
    return "API werkt ✔️"

@app.post("/scrape_zimmo")
def start_zimmo():
    data = request.get_json()
    postcodes_raw = data.get("postcodes", "")

    postcodes = []
    for part in postcodes_raw.split(","):
        part = part.strip()
        if not part:
            continue
        postcodes.append(part)

    for pc in postcodes:
        scrape_zimmo_html(pc, "koop")
        scrape_zimmo_html(pc, "huur")

    return jsonify({"status": "ok", "postcodes": postcodes})


if __name__ == "__main__":
    app.run()
