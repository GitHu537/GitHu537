import requests
import base64
import json
from hashlib import md5
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_file(file_data):
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(file_data, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

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