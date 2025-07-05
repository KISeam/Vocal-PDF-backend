from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Vocal PDF Backend is running!"})

@app.route("/get-pages", methods=["POST"])
def get_pages():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    reader = PdfReader(filepath)
    os.remove(filepath)
    return jsonify({"totalPages": len(reader.pages)})

@app.route("/read-preview", methods=["POST"])
def read_preview():
    file = request.files["file"]
    page_number = int(request.form["page"])
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    reader = PdfReader(filepath)

    if page_number < 1 or page_number > len(reader.pages):
        return jsonify({"error": "Invalid page number"}), 400

    text = reader.pages[page_number - 1].extract_text()
    os.remove(filepath)
    return jsonify({"text": text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
