from flask import Flask, request, jsonify, send_file
import os
from process_video import blur_faces

app = Flask(_name_)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    processed_path = os.path.join(PROCESSED_FOLDER, "processed_" + file.filename)
    
    file.save(file_path)
    blur_faces(file_path, processed_path)

    return jsonify({"message": "Processing complete", "processed_file": processed_path}), 200

@app.route("/download/<filename>", methods=["GET"])
def download_video(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, as_attachment=True)

if _name_ == "_main_":
    app.run(debug=True)
