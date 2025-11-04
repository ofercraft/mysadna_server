from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Dummy data ---
GEAR = [
    {
        "id": 1,
        "title": "מסור עגול",
        "description": "הנחיות בטיחות לשימוש במסור עגול.",
        "banner_image": "https://makeitsafe.b-cdn.net/circular_saw.jpg",
        "video": "https://stream.mux.com/qZ01wojcO41oS01KCeDNaJxcM00MWxMmrj3IXnG02vkBTRk.m3u8",
        "mankal": [
            "יש להשתמש במשקפי מגן ובאוזניות לפני תחילת העבודה",
            "אין להשתמש במכשיר אם כבל ההזנה פגום",
            "יש לכוון את המכשיר הרחק מכבל ההזנה",
            "יש לוודא שהגלגלת לא בלויה וכי היא תקינה ומשומנת כראוי",
            "חובה להשתמש רק בלהבים תקינים וחדים",
            "יש לוודא כי מסלול החיתוך נקי ממכשולים מעל ומתחת לחומר המעובד",
            "במהלך העבודה יש להרחיק את הידיים ממסלול החיתוך ומהלהב בפרט, ולהחזיק את המכשיר ביציבות בעזרת שתי הידיים",
            "יש להצמיד את המכשיר לחומר הגלם רק לאחר שהמסור מופעל",
            "אין לבלום את תנועת הלהב לאחר שחרור מתג ההפעלה. יש להמתין לסיום התנועה"
        ],
        "tags": ["safety", "woodworking", "power-tools"],
        "content": [
            {"type": "title", "value": "הקדמה"},
            {"type": "text", "value": "מסור עגול הוא כלי חשמלי עוצמתי המשמש לחיתוך עץ, מתכת וחומרים נוספים."},
            {"type": "image", "url": "https://makeitsafe.b-cdn.net/maxresdefault.jpg"},
            {"type": "warning", "value": "אין להסיר את מגן הלהב במהלך העבודה!"},
            {"type": "step", "value": "ודא שהמסור כבוי ומנותק מהחשמל לפני החלפת להב."},
            {"type": "text", "value": "לפני כל שימוש, יש לוודא כי הלהב חד, תקין, ומורכב כראוי."},
            {"type": "title", "value": "אמצעי בטיחות"},
            {"type": "text", "value": "יש להרכיב משקפי מגן, אוזניות, ולוודא שהאזור סביב נקי ממכשולים."},
            {"type": "video", "url": "https://stream.mux.com/qZ01wojcO41oS01KCeDNaJxcM00MWxMmrj3IXnG02vkBTRk.m3u8"}
        ]
    },
    {
        "id": 2,
        "title": "מקדחה",
        "description": "שימוש נכון ובטוח במקדחה חשמלית.",
        "banner_image": "https://makeitsafe.b-cdn.net/electric_drill.jpg",
        "video": "https://vz-48b0307b-989.b-cdn.net/f0aa39ae-cede-4583-83a0-f8ed7a68c63e/playlist.m3u8",
        "mankal": [
            "יש לוודא שהמקדחה מנותקת מהחשמל בזמן החלפת מקדח.",
            "אין להפעיל את המקדחה בסביבת נוזלים.",
            "יש לאחוז את הכלי בשתי ידיים בעת הקידוח."
        ],
        "tags": ["safety", "drilling"],
        "content": [
            {"type": "title", "value": "תיאור הכלי"},
            {"type": "text", "value": "המקדחה החשמלית משמשת לקידוח בחומרים שונים בהתאם לסוג המקדח."},
            {"type": "image", "url": "https://makeitsafe.b-cdn.net/electric_drill_2.jpg"},
            {"type": "step", "value": "בחר מקדח מתאים לחומר העבודה."},
            {"type": "warning", "value": "אין לקדוח בקרבת כבלי חשמל גלויים!"},
            {"type": "text", "value": "בעת העבודה, יש לשמור על יציבות הידיים ולמנוע החלקה."}
        ]
    }
]

# --- Possible tags ---
POSSIBLE_TAGS = [
    "safety", "protective-gear", "training", "inspection",
    "woodworking", "metalworking", "cutting", "drilling", "welding",
    "sanding", "machining", "electrical", "power-tools", "hand-tools",
    "cleaning", "maintenance", "setup", "storage",
    "wood", "metal", "plastic", "glass", "composite",
    "lab", "workshop", "production", "training-room"
]

# --- Possible content types ---
POSSIBLE_CONTENT_TYPES = [
    # Basic structure
    "title", "text", "image", "video",
    # Instructional
    "step", "tip", "note", "checklist",
    # Safety / Warnings
    "warning", "alert", "hazard",
    # Interactive or reference
    "pdf", "link", "download", "3d-model",
    # Organization
    "quote", "divider", "section", "list"
]

# --- Endpoints ---

@app.route("/api/gear", methods=["GET"])
def get_gear():
    """Return list of all gear items (summary info)."""
    result = [
        {
            "id": g["id"],
            "title": g["title"],
            "description": g["description"],
            "banner_image": g.get("banner_image"),
            "video": g.get("video"),
            "tags": g.get("tags", [])
        }
        for g in GEAR
    ]
    return jsonify(result)


@app.route("/api/gear/<int:gear_id>", methods=["GET"])
def get_gear_item(gear_id):
    """Return full gear item with all content and safety instructions."""
    gear = next((g for g in GEAR if g["id"] == gear_id), None)
    if not gear:
        return jsonify({"error": "Gear item not found"}), 404
    return jsonify(gear)


@app.route("/api/gear", methods=["POST"])
def create_gear_item():
    """Create a new gear item."""
    data = request.get_json()
    required_fields = ["title", "description", "banner_image", "content"]

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_gear = {
        "id": max((g["id"] for g in GEAR), default=0) + 1,
        "title": data["title"],
        "description": data["description"],
        "banner_image": data["banner_image"],
        "video": data.get("video"),
        "mankal": data.get("mankal", []),
        "tags": data.get("tags", []),
        "content": data["content"]
    }

    GEAR.append(new_gear)
    return jsonify(new_gear), 201


@app.route("/api/tags", methods=["GET"])
def get_tags():
    """Return list of possible tags for gear classification."""
    return jsonify(sorted(POSSIBLE_TAGS))


@app.route("/api/content-types", methods=["GET"])
def get_content_types():
    """Return list of supported content block types."""
    return jsonify(sorted(POSSIBLE_CONTENT_TYPES))


# --- Local testing ---
if __name__ == "__main__":
    app.run(debug=True)
