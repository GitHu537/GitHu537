const fs = require("fs");
const path = require("path");
const { encryptUsername } = require("../utils/md5Encrypt");
const { saveFile, getUserFiles } = require("../utils/fileUtils");

exports.uploadFile = async (req, res) => {
    const { username, category, encrypt } = req.body;
    const file = req.file;

    if (!username || !file) {
        return res.status(400).json({ message: "Username and file are required" });
    }

    const encryptedUsername = encryptUsername(username);
    const userDir = path.join(__dirname, "../uploads", encryptedUsername, category);

    // 确保目录存在
    fs.mkdirSync(userDir, { recursive: true });

    // 文件保存
    try {
        await saveFile(file, userDir, encrypt);

        const fileUrl = `/uploads/${encryptedUsername}/${category}/${file.filename}`;
        return res.status(200).json({ message: "File uploaded successfully", fileUrl });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: "File upload failed" });
    }
};

exports.getFileInfo = async (req, res) => {
    const { username } = req.params;
    const encryptedUsername = encryptUsername(username);

    try {
        const files = await getUserFiles(encryptedUsername);
        return res.status(200).json({ files });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: "Error retrieving files" });
    }
};