document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const file = document.getElementById('file').files[0];
    const category = document.getElementById('category').value;
    const encrypt = document.getElementById('encrypt').checked;

    const md5Username = md5(username); // MD5加密用户名

    const formData = new FormData();
    formData.append('username', md5Username);
    formData.append('file', file);
    formData.append('category', category);
    formData.append('encrypt', encrypt);

    const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    if (result.success) {
        document.getElementById('result').innerHTML = `
            <p>Upload successful!</p>
            <p><a href="${result.fileUrl}" target="_blank">Download Link</a></p>
        `;
    } else {
        document.getElementById('result').innerHTML = `<p>${result.message}</p>`;
    }
});