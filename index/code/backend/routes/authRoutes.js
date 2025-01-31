const express = require("express");
const authController = require("../controllers/authController");

const router = express.Router();

// 用户MD5加密处理
router.post("/encrypt", authController.encryptUsername);

module.exports = router;