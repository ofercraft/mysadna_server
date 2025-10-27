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
            "id": 101,
            "title": "Workshop Rules",
            "summary": "General conduct and safety rules for workshop classes (מרכז תה\"ל).",
            "content": """
                1. Every person (student, teacher, teaching assistant, etc.) must read and be familiar with the work procedures.
                2. Work is permitted only under the supervision of an instructor or certified teacher.
                3. Appropriate clothing must be worn (closed clothing, closed shoes).
                4. Entry into the workshop without the instructor’s permission is strictly prohibited.
                5. Proper behavior and mutual respect must be maintained.
                6. Do not work when tired, ill, or in any condition that could compromise safety.
                7. Do not operate any machine without prior instruction from the teacher.
                8. Any accident or malfunction must be reported immediately to the instructor.
                9. Safety goggles must be worn when working with cutting, sawing, or drilling tools.
                10. Tools and equipment must not be left in non-designated areas.
                11. The workspace must be kept clean and orderly at all times.
                12. At the end of the work session, make sure all electrical devices are turned off.
                13. The use of unauthorized electrical devices is strictly forbidden.
                14. Do not pass tools between students while working.
                15. Follow all rules for proper use of tools.
                16. Each student is responsible for the personal equipment assigned to them.
                17. Leaving the workshop is allowed only with the teacher’s permission.
                18. Working in the workshop requires responsibility and caution.
            """,
            "images": ["https://example.com/images/workshop_rules.jpg"]
        },
        {
            "id": 1000,
            "title": "Workshop closure",
            "summary": "End-of-session checklist for the workshop.",
            "content": """
                1. Make sure all devices are turned off.
                2. Make sure all materials are returned to their place.
                3. Return the equipment to the storage area.
                4. Report any shortages or damages to the teacher.
            """,
            "images": ["https://example.com/images/workshop_rules.jpg"]
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
    """Return a list of all guides (id + title)."""
    result = [{"id": g["id"], "title": g["title"]} for g in GUIDES]
    return jsonify(result)

@app.route("/api/guide/<int:guide_id>", methods=["GET"])
def get_guide(guide_id):
    """Return full guide data by ID."""
    guide = next((g for g in GUIDES if g["id"] == guide_id), None)
    if not guide:
        return jsonify({"error": "Guide not found"}), 404
    return jsonify(guide)

@app.route("/api/guides", methods=["POST"])
def create_guide():
    """Create a new guide and save it to file."""
    data = request.get_json()

    required_fields = ["title", "summary", "content"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_guide = {
        "id": max((g["id"] for g in GUIDES), default=0) + 1,
        "title": data["title"],
        "summary": data["summary"],
        "content": data["content"],
        "images": data.get("images", []),
    }

    GUIDES.append(new_guide)
    save_guides()

    return jsonify(new_guide), 201


# --- Local testing ---
if __name__ == "__main__":
    app.run(debug=True)
