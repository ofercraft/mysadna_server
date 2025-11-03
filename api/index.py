from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Dummy data ---
GUIDES = [
    {
        "id": 1,
        "title": "Jigsaw Basics",
        "description": "Learn how to safely and effectively use a jigsaw for woodworking.",
        "banner_image": "https://cdn.example.com/banners/jigsaw-banner.jpg",
        "tags": ["woodworking", "tools", "safety"],
        "content": [
            {"type": "title", "value": "Introduction"},
            {"type": "text", "value": "The jigsaw is a versatile power tool for making curved and straight cuts in wood, metal, or plastic."},
            {"type": "image", "url": "https://makeitsafe.b-cdn.net/maxresdefault.jpg"},
            {"type": "video", "url": "https://stream.mux.com/qZ01wojcO41oS01KCeDNaJxcM00MWxMmrj3IXnG02vkBTRk.m3u8"},
            {"type": "text", "value": "Always wear goggles and keep your hands away from the cutting path."},
            {"type": "title", "value": "Tips"},
            {"type": "text", "value": "Use the right blade for the material. Clamp your workpiece firmly before cutting."}
        ]
    },
    {
        "id": 2,
        "title": "Laser Cutter Setup",
        "description": "Step-by-step instructions for setting up and calibrating a laser cutter.",
        "banner_image": "https://cdn.example.com/banners/laser-setup.jpg",
        "tags": ["laser", "cutting", "setup"],
        "content": [
            {"type": "title", "value": "Overview"},
            {"type": "text", "value": "Before powering on the laser cutter, ensure the ventilation system is active."},
            {"type": "image", "url": "https://cdn.example.com/images/laser-cutter.jpg"},
            {"type": "video", "url": "https://stream.mux.com/abc123examplevideo.m3u8"},
            {"type": "text", "value": "Focus the laser lens using the calibration tool provided by the manufacturer."}
        ]
    },
    {
        "id": 3,
        "title": "3D Printing for Beginners",
        "description": "Your first steps into the world of additive manufacturing.",
        "banner_image": "https://cdn.example.com/banners/3dprinting.jpg",
        "tags": ["3d-printing", "maker"],
        "content": [
            {"type": "title", "value": "Welcome"},
            {"type": "text", "value": "3D printing turns digital models into physical objects layer by layer."},
            {"type": "image", "url": "https://cdn.example.com/images/3dprinter.jpg"},
            {"type": "video", "url": "https://stream.mux.com/example3dprint.m3u8"},
            {"type": "text", "value": "PLA is a great beginner filament—easy to print, minimal warping, and biodegradable."}
        ]
    }
]

# --- Endpoints ---

@app.route("/api/guides", methods=["GET"])
def get_guides():
    """Return list of all guides (summary info)."""
    result = [
        {
            "id": g["id"],
            "title": g["title"],
            "description": g["description"],
            "banner_image": g.get("banner_image"),
            "tags": g.get("tags", [])
        }
        for g in GUIDES
    ]
    return jsonify(result)

@app.route("/api/guide/<int:guide_id>", methods=["GET"])
def get_guide(guide_id):
    """Return full guide including structured content."""
    guide = next((g for g in GUIDES if g["id"] == guide_id), None)
    if not guide:
        return jsonify({"error": "Guide not found"}), 404
    return jsonify(guide)

@app.route("/api/guides", methods=["POST"])
def create_guide():
    """Create a new guide with title, description, banner_image, tags, and content."""
    data = request.get_json()
    required_fields = ["title", "description", "banner_image", "content"]

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_guide = {
        "id": max((g["id"] for g in GUIDES), default=0) + 1,
        "title": data["title"],
        "description": data["description"],
        "banner_image": data["banner_image"],
        "tags": data.get("tags", []),
        "content": data["content"]
    }

    GUIDES.append(new_guide)
    return jsonify(new_guide), 201

# --- Local testing ---
if __name__ == "__main__":
    app.run(debug=True)
