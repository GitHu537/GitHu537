from cryptography.fernet import Fernet
import os

# 假设密钥在GitHub Secrets中，使用一个固定的密钥进行示范
SECRET_KEY = b'your-secret-key-here'

# 加密文件
def encrypt_file(file, destination):
    fernet = Fernet(SECRET_KEY)
    with open(file.filename, 'rb') as original_file:
        original_data = original_file.read()
    encrypted_data = fernet.encrypt(original_data)

    with open(destination + '.enc', 'wb') as enc_file:
        enc_file.write(encrypted_data)

# 解密文件
def decrypt_file(file_path):
    fernet = Fernet(SECRET_KEY)
    with open(file_path, 'rb') as enc_file:
        encrypted_data = enc_file.read()
    
    decrypted_data = fernet.decrypt(encrypted_data)
    decrypted_file_path = file_path[:-4]  # 假设 .enc 后缀
    
    with open(decrypted_file_path, 'wb') as dec_file:
        dec_file.write(decrypted_data)
    
    return decrypted_file_path

# 检查文件类型是否有效
def is_valid_file_extension(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions