document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const queryForm = document.getElementById("query-form");
    const fileListDiv = document.getElementById("file-list");

    // 文件上传功能
    uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const category = document.getElementById("category").value;
        const fileInput = document.getElementById("file");
        const encrypt = document.getElementById("encrypt").checked;

        if (!fileInput.files.length) {
            alert("Please select a file.");
            return;
        }

        const formData = new FormData();
        formData.append("username", username);
        formData.append("category", category);
        formData.append("file", fileInput.files[0]);
        formData.append("encrypt", encrypt);

        try {
            const response = await fetch("/api/upload", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            if (response.ok) {
                alert("File uploaded successfully! Link: " + result.fileUrl);
            } else {
                alert("Error uploading file: " + result.message);
            }
        } catch (error) {
            alert("An error occurred: " + error.message);
        }
    });

    // 文件查询功能
    queryForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const username = document.getElementById("query-username").value;

        try {
            const response = await fetch(`/api/file-info/${username}`);
            const result = await response.json();

            if (response.ok) {
                fileListDiv.innerHTML = "";
                result.files.forEach((file) => {
                    const fileDiv = document.createElement("div");
                    fileDiv.classList.add("file-item");
                    fileDiv.innerHTML = `
                        <p><strong>File Name:</strong> ${file.name}</p>
                        <p><strong>Category:</strong> ${file.category}</p>
                        <p><strong>Encrypted:</strong> ${file.isEncrypted ? "Yes" : "No"}</p>
                        <button onclick="copyLink('${file.name}')">Copy Link</button>
                    `;
                    fileListDiv.appendChild(fileDiv);
                });
            } else {
                alert("Error retrieving files: " + result.message);
            }
        } catch (error) {
            alert("An error occurred: " + error.message);
        }
    });
});

// 复制链接功能
function copyLink(fileName) {
    const link = `${window.location.origin}/uploads/${fileName}`;
    navigator.clipboard.writeText(link).then(() => {
        alert("Link copied to clipboard!");
    });
}