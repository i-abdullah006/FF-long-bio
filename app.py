from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote

app = Flask(__name__)

# Apni API key yahan lagao
API_KEY = "paglu_dev"
API_BASE_URL = "https://bio.ffutils.tech/api/update_bio"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/update-bio", methods=["POST"])
def update_bio():
    try:
        data = request.get_json()

        token = data.get("access_token", "").strip()
        bio = data.get("bio", "").strip()

        if not token:
            return jsonify({
                "success": False,
                "message": "Access token is required."
            }), 400

        if not bio:
            return jsonify({
                "success": False,
                "message": "Bio is required."
            }), 400

        url = (
            f"{API_BASE_URL}"
            f"?access_token={token}"
            f"&bio={quote(bio, safe='')}"
            f"&key={API_KEY}"
        )

        response = requests.get(url, timeout=15)
        result = response.json()

        if result.get("status") == "success":
            return jsonify({
                "success": True,
                "player_name": result.get("nickname", "Unknown"),
                "uid": result.get("uid", "N/A"),
                "region": result.get("region", "N/A"),
                "bio": result.get("bio", bio)
            })

        return jsonify({
            "success": False,
            "message": result.get("message", "Failed to update bio.")
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
