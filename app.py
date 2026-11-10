
import os
from flask import Flask, request, jsonify
from google_play_scraper import reviews, Sort

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "online", "service": "ProductIQ Google Play Scraper"})

@app.route("/reviews", methods=["GET"])
def get_reviews():
    package_name = request.args.get("app_id")
    count = min(int(request.args.get("count", 100)), 200)

    if not package_name:
        return jsonify({"error": "Please provide app_id"}), 400

    try:
        result, _ = reviews(
            package_name,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=count
        )

        return jsonify({
            "app_id": package_name,
            "count": len(result),
            "reviews": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
