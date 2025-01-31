from flask import Flask, send_file, abort
from Crypto.Cipher import AES
import requests
from io import BytesIO
import hashlib
import os

app = Flask(__name__)

# 从 GitHub Secrets 获取密钥（环境变量中配置）
SECRET_KEY = os.environ.get('ENCRYPTION_KEY')  # 例如 'mysecretkey12345'

# 解密函数
def decrypt_file(encrypted_data, key):
    """解密文件"""
    nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        raise ValueError("Decryption failed or data is corrupted.")
    return plaintext

# 从 GitHub 获取加密文件的内容
def fetch_encrypted_file_from_github(user_md5, file_category, filename):
    """从 GitHub 仓库下载加密文件"""
    # 构造文件的 GitHub URL
    github_url = f'https://raw.githubusercontent.com/username/repository/main/UserFiles/Files/{user_md5}/{file_category}/{filename}.enc'
    response = requests.get(github_url)
    
    if response.status_code == 200:
        return response.content
    else:
        raise Exception("Failed to fetch file from GitHub.")

# 处理文件解密并提供下载
@app.route('/download/<username>/<file_category>/<filename>', methods=['GET'])
def download_file(username, file_category, filename):
    """下载解密文件"""
    try:
        # 计算用户名的 MD5 值
        user_md5 = hashlib.md5(username.encode('utf-8')).hexdigest()

        # 获取加密文件数据
        encrypted_data = fetch_encrypted_file_from_github(user_md5, file_category, filename)

        # 解密文件
        decrypted_data = decrypt_file(encrypted_data, SECRET_KEY)
        
        # 返回解密后的文件作为响应
        return send_file(BytesIO(decrypted_data), as_attachment=True, download_name=filename)
    
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
