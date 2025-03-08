from flask import Flask, request,jsonify, send_file
import os
app = Flask(_name_)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route("/upload",methods=["POST"])
def upload_video():
 if "file"not in request.files:
  return jsonify({"error": "No file part"}), 400
file = request.files["file"]
if file.filename == "":
 return jsonify({"error": "No selected file "}), 400
file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
file.save(file_path)
return jsonify({"message": "File uploaded successfully" , "file_path":file_path}), 200
@app.route("/download/<filename>",methods=["GET"])
def download_video(filename):
 file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
if not os.path.exists(file_path):
 return jsonify({"error": "File not Found"}) , 404
return send_file(file_path, as_attachment=True)
if_name_ == "_main_":
app.run(host="0.0.0.0" , port=5000)
