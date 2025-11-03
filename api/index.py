from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

GUIDES_FILE = "guides.json"

# --- Load guides from file or default data ---
def load_guides():
    if os.path.exists(GUIDES_FILE):
        with open(GUIDES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return [
        {
            "id": 1,
            "title": "Workshop Safety Overview",
            "description": "Essential safety instructions for using the workshop safely.",
            "video_url": "https://stream.mux.com/qZ01wojcO41oS01KCeDNaJxcM00MWxMmrj3IXnG02vkBTRk.m3u8"
        },
        {
            "id": 2,
            "title": "לילה לבן",
            "description": "הזמנה ללילה הלבן של המחוננים",
            "video_url": "https://vz-48b0307b-989.b-cdn.net/3653ae58-a323-47e8-86b4-f2929352f13b/playlist.m3u8"
        },
        {
            "id": 3,
            "title": "לירן ועודד האהובים",
            "description": "סרטון של לירן ועודד",
            "video_url": "https://stream.mux.com/bPbD4ACWzCPownH9P7RfTtpYryB1yNhtTb01BIqysWkE"
        },
    ]

GUIDES = load_guides()

# --- Utility ---
def save_guides():
    with open(GUIDES_FILE, "w", encoding="utf-8") as f:
        json.dump(GUIDES, f, ensure_ascii=False, indent=2)

# --- Endpoints ---

@app.route("/api/guides", methods=["GET"])
def get_guides():
    """Return list of all guides with id, title, and description."""
    result = [{"id": g["id"], "title": g["title"], "description": g["description"]} for g in GUIDES]
    return jsonify(result)

@app.route("/api/guide/<int:guide_id>", methods=["GET"])
def get_guide(guide_id):
    """Return full guide data including video URL."""
    guide = next((g for g in GUIDES if g["id"] == guide_id), None)
    if not guide:
        return jsonify({"error": "Guide not found"}), 404
    return jsonify(guide)

@app.route("/api/guides", methods=["POST"])
def create_guide():
    """Create a new guide with title, description, and video_url."""
    data = request.get_json()

    required_fields = ["title", "description", "video_url"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_guide = {
        "id": max((g["id"] for g in GUIDES), default=0) + 1,
        "title": data["title"],
        "description": data["description"],
        "video_url": data["video_url"]
    }

    GUIDES.append(new_guide)
    save_guides()

    return jsonify(new_guide), 201

# --- Local testing ---
if __name__ == "__main__":
    app.run(debug=True)
