from flask import Flask, request, jsonify
from hashlib import md5
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import requests
import magic

app = Flask(__name__)

# 从环境变量获取 GitHub 相关信息
GITHUB_API_URL = os.environ.get('GITHUB_API_URL')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_NAME = os.environ.get('REPO_NAME')

# 加密文件的密钥（存储在 GitHub Secrets 中）
SECRET_KEY = os.environ.get('SECRET_KEY')

def encrypt_file(file_data):
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(file_data, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def decrypt_file(iv, ct):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

def get_file_type(file_name):
    mime = magic.Magic(mime=True)
    return mime.from_file(file_name)

def upload_to_github(file_path, file_name, folder_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    iv, ct = encrypt_file(file_data)
    encoded_content = json.dumps({
        'message': 'Upload encrypted file',
        'content': ct,
        'sha': None
    })
    
    url = f'{GITHUB_API_URL}/repos/{REPO_NAME}/contents/{folder_path}/{file_name}'
    
    response = requests.put(url, headers={'Authorization': f'token {GITHUB_TOKEN}'}, data=encoded_content)
    
    return response.json()

@app.route('/upload', methods=['POST'])
def upload_file():
    username = request.form.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    file_name = file.filename
    file_type = get_file_type(file_name)

    # 加密后的用户名MD5
    user_md5 = md5(username.encode('utf-8')).hexdigest()

    # 生成文件夹路径
    folder_path = f'UserFiles/Files/{user_md5}/{file_type}'
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)

    file.save(file_path)

    # 上传到 GitHub
    response = upload_to_github(file_path, file_name, folder_path)
    
    if 'content' not in response:
        return jsonify({'error': 'Failed to upload file to GitHub'}), 500
    
    return jsonify({'message': 'File uploaded successfully', 'file_url': response['content']['download_url']})


if __name__ == '__main__':
    app.run(debug=True)