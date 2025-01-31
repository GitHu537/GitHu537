from flask import Flask, request, jsonify
import os
import hashlib
from upload_to_github import upload_to_github

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # 获取上传的文件和用户名
        file = request.files.get('file')
        username = request.form.get('username')

        if not file or not username:
            return jsonify({'success': False, 'error': 'File and username are required'}), 400

        # MD5 加密用户名
        user_md5 = hashlib.md5(username.encode()).hexdigest()

        # 保存文件到临时路径
        file_path = f'./tmp/{file.filename}'
        file.save(file_path)

        # 设置 GitHub Token
        token = os.getenv('GITHUB_TOKEN')  # 从环境变量中获取 GitHub Token

        # 调用上传至 GitHub 的函数
        response_status, response_text = upload_to_github(file_path, user_md5, '未分类', file.filename, token)
        if response_status == 201:
            download_url = f'https://raw.githubusercontent.com/{os.getenv("GITHUB_USERNAME")}/{os.getenv("GITHUB_REPO")}/main/UserFiles/Files/{user_md5}/未分类/{file.filename}'
            return jsonify({'success': True, 'downloadUrl': download_url})

        else:
            return jsonify({'success': False, 'error': f"Upload failed: {response_text}"}), 500

    except Exception as e:
        # 记录详细错误信息
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)