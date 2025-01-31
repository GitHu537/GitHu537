from flask import Flask, request, jsonify, send_from_directory
import hashlib
import os
from werkzeug.utils import secure_filename
from utils import encrypt_file, decrypt_file, is_valid_file_extension
import mimetypes

app = Flask(__name__)

# 配置文件夹路径
UPLOAD_FOLDER = 'index/UserFiles/Files'
ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'pdf', 'zip', 'jpg', 'png'}  # 支持的文件类型
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key_here'

# 上传文件API
@app.route('/upload', methods=['POST'])
def upload_file():
    username_md5 = request.form['username_md5']
    file_category = request.form['file_category']
    file = request.files['file']
    encrypt = request.form.get('encrypt', 'false') == 'true'

    if not is_valid_file_extension(file.filename, ALLOWED_EXTENSIONS):
        return jsonify({"error": "Invalid file type."}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], username_md5, file_category, filename)

    # 创建用户文件夹路径
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if encrypt:
        encrypt_file(file, file_path)
    else:
        file.save(file_path)

    # 生成文件的直链
    file_link = f"/files/{username_md5}/{file_category}/{filename}"

    return jsonify({"message": "Upload successful", "file_link": file_link}), 200

# 查询文件API
@app.route('/files/<username_md5>/<file_category>/<filename>', methods=['GET'])
def download_file(username_md5, file_category, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], username_md5, file_category, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found."}), 404

    # 如果是加密文件，解密后再提供
    if filename.endswith('.enc'):  # 假设加密文件以 .enc 后缀
        file_path = decrypt_file(file_path)

    # 获取文件的 MIME 类型
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'application/octet-stream'
    
    return send_from_directory(os.path.dirname(file_path), filename, mimetype=mime_type)

if __name__ == '__main__':
    app.run(debug=True)