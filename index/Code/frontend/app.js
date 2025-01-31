document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const file = document.getElementById('file').files[0];
    const category = document.getElementById('file-category').value;
    const encrypt = document.getElementById('encrypt').checked;

    const formData = new FormData();
    formData.append('username_md5', md5(username));
    formData.append('file', file);
    formData.append('file_category', category);
    formData.append('encrypt', encrypt ? 'true' : 'false');

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.file_link) {
            document.getElementById('result').innerHTML = `Upload Successful! <a href="${data.file_link}" target="_blank">Download File</a>`;
        } else {
            document.getElementById('result').innerHTML = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `Error: ${error.message}`;
    });
});