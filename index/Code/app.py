import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 设置文件上传目录
UPLOAD_FOLDER = 'uploads'  # 设置文件存储的文件夹，当前目录下的 uploads 文件夹
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf', 'mp4'}  # 可上传的文件类型
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查文件扩展名是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # 获取安全的文件名
        filename = secure_filename(file.filename)
        # 拼接文件的存储路径
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # 创建文件夹（如果文件夹不存在的话）
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        # 保存文件
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'message': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)