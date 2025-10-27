from flask import Flask, jsonify, request
import os

app = Flask(__name__)

GUIDES = [
    {
        "id": 101,
        "title": "Safety Basics",
        "summary": "Quick rules for tool use and sadna behavior.",
        "content": """
        - Always wear protective gear.
        - Check your workspace before starting.
        - Turn off tools before adjusting or cleaning.
        """,
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxaI9QkVCaPLwcmmm21-GyUzJSLxycu00K0A&s",
            "https://cdn11.bigcommerce.com/s-n7dyokm269/images/stencil/1280x1280/products/378/1859/SafetyFirst__88603.1554394304.gif?c=2"
        ]
    },
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
        "id": 3,
        "title": "Soldering 101",
        "summary": "Tin, join, clean. Do and don’ts.",
        "content": """
        - Always use a fume extractor.
        - Tin your tip before use.
        - Clean the joint after soldering.
        """,
        "images": [
            "https://www.ifixit.com/_next/image?url=https%3A%2F%2Fifixit-strapi-uploads.s3.us-east-1.amazonaws.com%2FCollection_Page_Headers_Soldering_d886934323.jpg&w=3840&q=75"
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
    {
        "id": 5,
        "title": "Workshop Rules - נהלי עבודה תשע\"ח",
        "summary": "General conduct and safety rules for workshop classes (מרכז תה\"ל).",
        "content": """
        ### דרישות כלליות
        1. כל אדם (תלמיד, מורה, תומך הוראה וכו') חייב לקרוא ולהכיר את נהלי העבודה.
        2. חובה לעבוד רק תחת פיקוח מדריך או מורה מוסמך.
        3. יש להגיע בלבוש מתאים (בגדים סגורים, נעליים סגורות).
        4. חל איסור על כניסה לסדנה ללא אישור מדריך.
        5. יש לשמור על התנהגות נאותה וכבוד הדדי.
        6. אין לעבוד כאשר האדם עייף, חולה או במצב שעלול לפגוע בבטיחותו.
        7. אין להפעיל מכונה ללא הדרכה מוקדמת מהמורה.
        8. יש לדווח מיד על כל תאונה או תקלה למדריך.
        9. חובה להרכיב משקפי מגן בכל עבודה עם כלי חיתוך, ניסור או קידוח.
        10. אין להשאיר כלים או ציוד במקומות שאינם ייעודיים לכך.
        11. חובה לשמור על סדר וניקיון במקום העבודה.
        12. בתום העבודה יש לוודא כיבוי כל המכשירים החשמליים.
        13. חל איסור על שימוש במכשירים חשמליים שאינם מאושרים.
        14. אין להעביר כלים בין תלמידים בזמן עבודה.
        15. יש לשמור על כללים של שימוש נכון בכלי עבודה.
        16. כל תלמיד אחראי לציוד האישי שסופק לו.
        17. יציאה מהסדנה רק באישור המורה.
        18. תחום העבודה בסדנה מחייב אחריות וזהירות.

        ### הוראות לסגירת הסדנה
        1. לוודא שכל המכשירים כבויים.
        2. לוודא שכל החומרים חוזרים למקומם.
        3. להחזיר ציוד למקום האחסון.
        4. לדווח למורה על חוסרים או נזקים.
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
