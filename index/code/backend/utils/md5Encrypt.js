const crypto = require("crypto");

exports.encryptUsername = (username) => {
    const md5Hash = crypto.createHash("md5");
    return md5Hash.update(username).digest("hex");
};