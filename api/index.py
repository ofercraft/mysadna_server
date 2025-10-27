from flask import Flask, jsonify, request
import os

app = Flask(__name__)

GUIDES = [
    {
        "id": 2,
        "title": "3D Printer Setup",
        "summary": "Bed leveling, filament loading, test print.",
        "content": """
        1. Level the bed using the calibration knobs.
        [IMAGE:0]
        2. Load filament by heating the nozzle and inserting material.
        [IMAGE:1]
        3. Run a small cube test print before starting.
        """,
        "images": [
            "https://cdn1.bambulab.com/x1/x1Series-main-bg-v1.png",
            "https://cdn11.bigcommerce.com/s-n7dyokm269/images/stencil/1280x1280/products/378/1859/SafetyFirst__88603.1554394304.gif?c=2"
        ]
    },
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
        "images": [
            "https://example.com/images/workshop_rules.jpg"
        ]
    },
    {
        "id": 1000,
        "title": "Workshop closure",
        "summary": "General conduct and safety rules for workshop classes (מרכז תה\"ל).",
        "content": """
1. Make sure all devices are turned off.
2. Make sure all materials are returned to their place.
3. Return the equipment to the storage area.
4. Report any shortages or damages to the teacher.
        """,
        "images": [
            "https://example.com/images/workshop_rules.jpg"
        ]
    }
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
