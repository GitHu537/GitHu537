const { encryptUsername } = require("../utils/md5Encrypt");

exports.encryptUsername = (req, res) => {
    const { username } = req.body;
    if (!username) {
        return res.status(400).json({ message: "Username is required" });
    }

    const encryptedUsername = encryptUsername(username);
    return res.status(200).json({ encryptedUsername });
};