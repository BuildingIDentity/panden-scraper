from flask import Flask, request, jsonify
from scrapers.zimmo_html import scrape_zimmo_html

app = Flask(__name__)

def parse_postcodes(input_str):
    pcs = set()
    parts = input_str.split(",")
    for p in parts:
        p = p.strip()
        if "-" in p:
            s, e = p.split("-")
            for x in range(int(s), int(e)+1):
                pcs.add(str(x))
        else:
            pcs.add(p)
    return sorted(pcs)

@app.route("/")
def home():
    return jsonify({"status": "online"})

@app.post("/scrape_zimmo")
def start_zimmo():
    data = request.get_json() or {}
    raw = data.get("postcodes", "")
    postcodes = parse_postcodes(raw)

    for pc in postcodes:
        scrape_zimmo_html(pc, "koop")
        scrape_zimmo_html(pc, "huur")

    return jsonify({"status": "ok", "postcodes": postcodes})

if __name__ == "__main__":
    app.run()
