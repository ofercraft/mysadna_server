from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Dummy data ---
GEAR = [
    {
        "id": 1,
        "title": "מסור עגול - Circular Saw",
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
            {"type": "text", "value": "לפני כל שימוש, יש לוודא כי הלהב חד, תקין, ומורכב כראוי."},
            {"type": "title", "value": "אמצעי בטיחות"},
            {"type": "text", "value": "יש להרכיב משקפי מגן, אוזניות, ולוודא שהאזור סביב נקי ממכשולים."}
        ]
    },
    {
        "id": 2,
        "title": "מקדחה - Electric Drill",
        "description": "שימוש נכון ובטוח במקדחה חשמלית.",
        "banner_image": "https://cdn.example.com/banners/drill-banner.jpg",
        "video": "https://stream.mux.com/exampledrillvideo.m3u8",
        "mankal": [
            "יש לוודא שהמקדחה מנותקת מהחשמל בזמן החלפת מקדח.",
            "אין להפעיל את המקדחה בסביבת נוזלים.",
            "יש לאחוז את הכלי בשתי ידיים בעת הקידוח."
        ],
        "tags": ["safety", "drilling"],
        "content": [
            {"type": "title", "value": "תיאור הכלי"},
            {"type": "text", "value": "המקדחה החשמלית משמשת לקידוח בחומרים שונים בהתאם לסוג המקדח."},
            {"type": "image", "url": "https://cdn.example.com/images/drill.jpg"},
            {"type": "text", "value": "בעת העבודה, יש לשמור על יציבות הידיים ולמנוע החלקה."}
        ]
    }
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

# --- Local testing ---
if __name__ == "__main__":
    app.run(debug=True)
