const express = require("express");
const fileController = require("../controllers/fileController");
const multer = require("multer");
const upload = multer({ dest: "uploads/" });

const router = express.Router();

// 上传文件
router.post("/upload", upload.single("file"), fileController.uploadFile);

// 查询文件
router.get("/file-info/:username", fileController.getFileInfo);

module.exports = router;