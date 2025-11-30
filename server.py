from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/")
def index():
    return "API draait ✔️"

@app.post("/scrape_zimmo")
def scrape_zimmo():
    try:
        data = request.get_json()
        postcodes = data.get("postcodes", "")

        # tijdelijk voor test
        print("Binnenkomende postcodes:", postcodes)

        return jsonify({
            "status": "ok",
            "message": "scraper zou nu draaien",
            "postcodes": postcodes
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Heroku start ALTIJD hierop
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
