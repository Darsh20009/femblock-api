from flask import Flask, request, jsonify, send_file
import os
from process_video import blur_faces

app = Flask(_name_)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    processed_path = os.path.join(PROCESSED_FOLDER, "processed_" + file.filename)

    file.save(file_path)
    blur_faces(file_path, processed_path)

    return jsonify({"message": "Processing complete", "processed_file": file.filename}), 200

@app.route("/download/<filename>", methods=["GET"])
def download_video(filename):
    file_path = os.path.join(PROCESSED_FOLDER, "processed_" + filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, as_attachment=True)

if _name_ == "_main_":
    app.run(debug=True, host="0.0.0.0", port=5000)
