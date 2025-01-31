from Crypto.Cipher import AES
import hashlib

def encrypt_file(file_path, key):
    """加密文件并保存"""
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    # 保存加密文件
    with open(file_path + '.enc', 'wb') as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]

def upload_to_github(file_path, encrypted_file_path, username_md5, category):
    """将加密后的文件上传到 GitHub 仓库"""
    # 使用 GitHub API 或 GitHub CLI 上传文件到正确的目录
    # 这里假设上传脚本已经配置好并能够将文件上传到仓库
    pass  # 你可以使用 GitHub Actions 或 GitHub API 来自动化上传
