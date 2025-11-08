from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# ---------- Initialize Firebase ----------
SERVICE_ACCOUNT_JSON = {
    "type": "service_account",
    "project_id": "m4keitsafe",
    "private_key_id": "d5fc4ac075398de9c866dd45c11b422ebdc54cd6",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkq..."
                   "-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fbsvc@m4keitsafe.iam.gserviceaccount.com",
    "client_id": "116512063567980832596",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40m4keitsafe.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_JSON)
    firebase_admin.initialize_app(cred)
    print("✅ Firebase initialized")

db = firestore.client()


# ---------- ROUTES ----------

@app.route("/api/tools", methods=["GET"])
def get_tools():
    """Return all tools (id + name + banner)."""
    tools_ref = db.collection("tools")
    docs = tools_ref.stream()
    tools = []
    for doc in docs:
        data = doc.to_dict()
        tools.append({
            "id": doc.id,
            "name": data.get("name"),
            "banner": data.get("banner", None)
        })
    return jsonify(tools), 200


@app.route("/api/tool/<path:tool_id>", methods=["GET"])
def get_tool(tool_id):
    """Return a specific tool with its guide steps."""
    tool_ref = db.collection("tools").document(tool_id)
    tool_doc = tool_ref.get()

    if not tool_doc.exists:
        return jsonify({"error": f"Tool '{tool_id}' not found"}), 404

    data = tool_doc.to_dict() or {}
    data["id"] = tool_id

    # Include subcollection "guide"
    guide_ref = tool_ref.collection("guide")
    guide_docs = guide_ref.stream()
    guide_steps = []
    for step in guide_docs:
        guide_steps.append({
            "id": step.id,
            **(step.to_dict() or {})
        })

    # Sort steps by Firestore ID order if applicable
    data["guide"] = sorted(guide_steps, key=lambda s: s["id"])

    return jsonify(data), 200


@app.route("/api/tools", methods=["POST"])
def create_tool():
    """Create a new tool document with optional banner."""
    data = request.get_json(force=True)
    required = ["name"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    tool_ref = db.collection("tools").document(data["name"].replace(" ", "_").lower())
    tool_ref.set({
        "name": data["name"],
        "mancal": data.get("mancal", []),
        "video": data.get("video", ""),
        "banner": data.get("banner", None)
    })
    return jsonify({"status": "created", "id": tool_ref.id}), 201


@app.route("/api/tool/<tool_id>/guide", methods=["POST"])
def add_guide_step(tool_id):
    """Add a guide step (text/image/title/divider) to a tool."""
    data = request.get_json(force=True)
    required = ["type"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required 'type' field"}), 400

    tool_ref = db.collection("tools").document(tool_id)
    if not tool_ref.get().exists:
        return jsonify({"error": f"Tool '{tool_id}' not found"}), 404

    guide_ref = tool_ref.collection("guide").document()
    guide_ref.set({
        "type": data["type"],
        "value": data.get("value", "")
    })
    return jsonify({
        "status": "added",
        "tool_id": tool_id,
        "guide_step_id": guide_ref.id
    }), 201


@app.route("/api/tool/<tool_id>/guide/<step_id>", methods=["PATCH"])
def update_guide_step(tool_id, step_id):
    """Update a specific guide step (e.g., change text or type)."""
    data = request.get_json(force=True)
    tool_ref = db.collection("tools").document(tool_id)
    step_ref = tool_ref.collection("guide").document(step_id)

    if not step_ref.get().exists:
        return jsonify({"error": f"Guide step '{step_id}' not found"}), 404

    step_ref.update(data)
    return jsonify({"status": "updated", "id": step_id}), 200


@app.route("/api/tool/<tool_id>/guide/<step_id>", methods=["DELETE"])
def delete_guide_step(tool_id, step_id):
    """Delete a specific guide step."""
    tool_ref = db.collection("tools").document(tool_id)
    step_ref = tool_ref.collection("guide").document(step_id)

    if not step_ref.get().exists:
        return jsonify({"error": f"Guide step '{step_id}' not found"}), 404

    step_ref.delete()
    return jsonify({"status": "deleted", "id": step_id}), 200


if __name__ == "__main__":
    app.run(debug=True)
