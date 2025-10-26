from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Simple in-memory data for guides
GUIDES = [
    {
        "id": 101,
        "title": "Safety Basics",
        "summary": "Quick rules for tool use and lab behavior.",
        "content": """
        ### Safety Basics
        - Always wear protective gear.
        - Check your workspace before starting.
        - Turn off tools before adjusting or cleaning.
        """,
        "images": [
            "https://example.com/images/safety_gear.jpg",
            "https://example.com/images/tool_rules.jpg"
        ]
    },
    {
        "id": 2,
        "title": "3D Printer Setup",
        "summary": "Bed leveling, filament loading, test print.",
        "content": """
        ### 3D Printer Setup
        1. Level the bed using the calibration knobs.
        2. Load filament by heating the nozzle and inserting material.
        3. Run a small cube test print before starting.
        """,
        "images": [
            "https://example.com/images/printer_setup.jpg"
        ]
    },
    {
        "id": 3,
        "title": "Soldering 101",
        "summary": "Tin, join, clean. Do and don’ts.",
        "content": """
        ### Soldering 101
        - Always use a fume extractor.
        - Tin your tip before use.
        - Clean the joint after soldering.
        """,
        "images": [
            "https://example.com/images/soldering_tips.jpg"
        ]
    },
    {
        "id": 4,
        "title": "Inventory QR Tips",
        "summary": "Labeling and scanning best practices.",
        "content": """
        ### Inventory QR Tips
        - Use high-contrast labels.
        - Keep them in visible spots.
        - Test scanning range before deploying.
        """,
        "images": [
            "https://example.com/images/qr_labels.jpg"
        ]
    },
]

@app.route("/api/guides", methods=["GET"])
def get_guides():
    """Return a simple list of all guides with id and title only."""
    result = [{"id": g["id"], "title": g["title"]} for g in GUIDES]
    return jsonify(result)

@app.route("/api/guide/<int:guide_id>", methods=["GET"])
def get_guide(guide_id):
    """Return full guide data by ID (text + images)."""
    guide = next((g for g in GUIDES if g["id"] == guide_id), None)
    if not guide:
        return jsonify({"error": "Guide not found"}), 404
    return jsonify(guide)

# For local testing
if __name__ == "__main__":
    app.run(debug=True)
