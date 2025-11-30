from flask import Flask, request, jsonify
from scrapers.zimmo_html import scrape_zimmo_html

app = Flask(__name__)

@app.get("/")
def index():
    return "API draait ✔️"

# --- POST /scrape_zimmo ---
@app.post("/scrape_zimmo")
def scrape_zimmo():
    try:
        data = request.get_json()
        postcodes_str = data.get("postcodes", "")

        if not postcodes_str:
            return jsonify({"status": "error", "message": "Geen postcodes ontvangen"}), 400

        # string → lijst postcodes
        postcodes = [pc.strip() for pc in postcodes_str.split(",")]

        print("Binnenkomende postcodes:", postcodes)

        results = []

        for pc in postcodes:
            # koop
            try:
                scrape_zimmo_html(pc, "koop")
                results.append({"postcode": pc, "type": "koop", "status": "ok"})
            except Exception as e:
                results.append({"postcode": pc, "type": "koop", "status": "error", "error": str(e)})

            # huur
            try:
                scrape_zimmo_html(pc, "huur")
                results.append({"postcode": pc, "type": "huur", "status": "ok"})
            except Exception as e:
                results.append({"postcode": pc, "type": "huur", "status": "error", "error": str(e)})

        return jsonify({
            "status": "ok",
            "postcodes": postcodes,
            "results": results
        })

    except Exception as e:
        print("Fout in scrape_zimmo:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# --- TEST ENDPOINT ---
@app.get("/test_zimmo")
def test_zimmo():
    try:
        scrape_zimmo_html("9000", "koop")
        return {"status": "ok", "message": "Test scrape uitgevoerd (koop 9000)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
