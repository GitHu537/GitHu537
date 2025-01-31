import os
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def encrypt_file(file_path, key):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(file_path, 'rb') as f:
        file_data = f.read()
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
    return cipher.iv + encrypted_data  # 返回IV和加密后的数据

def upload_to_github(file_path, user_md5, category, filename, token):
    try:
        # 获取 GitHub API 的 URL
        repo_name = os.getenv("GITHUB_REPO")
        username = os.getenv("GITHUB_USERNAME")
        url = f"https://api.github.com/repos/{username}/{repo_name}/contents/UserFiles/Files/{user_md5}/{category}/{filename}"

        # 获取加密密钥
        key = os.getenv("ENCRYPTION_KEY").encode('utf-8')

        # 加密文件
        encrypted_data = encrypt_file(file_path, key)

        # 将加密后的文件内容编码为 base64
        encoded_file_data = base64.b64encode(encrypted_data).decode('utf-8')

        # GitHub API 请求头
        headers = {
            'Authorization': f'token {token}',
            'Content-Type': 'application/json',
        }

        # 请求数据
        data = {
            'message': f'Upload {filename}',
            'content': encoded_file_data,
        }

        # 发送请求到 GitHub API
        response = requests.put(url, json=data, headers=headers)

        # 检查响应
        if response.status_code == 201:
            return response.status_code, 'Upload successful'
        else:
            return response.status_code, response.text

    except Exception as e:
        return 500, str(e)