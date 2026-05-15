from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory store
notes = [
    {"id": 1, "title": "Welcome!", "body": "This is your first note. Edit or delete it.", "created": "2026-05-15"},
    {"id": 2, "title": "Flask + React", "body": "A simple full-stack app powered by Flask and React.", "created": "2026-05-15"},
]
next_id = 3

@app.route("/api/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)

@app.route("/api/notes", methods=["POST"])
def create_note():
    global next_id
    data = request.get_json()
    note = {
        "id": next_id,
        "title": data.get("title", "Untitled"),
        "body": data.get("body", ""),
        "created": datetime.today().strftime("%Y-%m-%d"),
    }
    notes.append(note)
    next_id += 1
    return jsonify(note), 201

@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return jsonify({"message": "Deleted"}), 200

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "time": datetime.now().isoformat()})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
