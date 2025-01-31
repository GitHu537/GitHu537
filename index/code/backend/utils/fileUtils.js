const fs = require("fs");
const path = require("path");

// 保存文件
exports.saveFile = (file, dir, encrypt) => {
    return new Promise((resolve, reject) => {
        const filePath = path.join(dir, file.filename);
        
        // 这里可以添加加密逻辑
        if (encrypt) {
            // 加密文件的处理逻辑
        }
        
        // 保存文件
        fs.rename(file.path, filePath, (err) => {
            if (err) return reject(err);
            resolve(filePath);
        });
    });
};

// 获取用户文件列表
exports.getUserFiles = (username) => {
    return new Promise((resolve, reject) => {
        const userDir = path.join(__dirname, "../uploads", username);

        fs.readdir(userDir, (err, files) => {
            if (err) return reject(err);
            const fileDetails = files.map((file) => {
                const stats = fs.statSync(path.join(userDir, file));
                return {
                    name: file,
                    category: path.dirname(file),
                    isEncrypted: stats.isEncrypted || false,  // 示例，实际需要按逻辑判断
                };
            });
            resolve(fileDetails);
        });
    });
};