document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('upload-btn').addEventListener('click', uploadFile);
    document.getElementById('set-index-target-btn').addEventListener('click', setIndexAndTarget);
});

function uploadFile() {
    let formData = new FormData(document.getElementById('upload-form'));
    fetch('/uploadfile', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error uploading file:', data.error);
            showMessage('Error uploading file', 'error');
        } else {
            populateColumnSelectors(data.columns);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        showMessage('Error in file upload', 'error');
    });
}

function populateColumnSelectors(columns) {
    columns.sort();

    let indexSelector = document.getElementById('index-column-list');
    let targetSelector = document.getElementById('target-column-list');

    indexSelector.innerHTML = '';
    targetSelector.innerHTML = '';

    columns.forEach(column => {
        let option = document.createElement('option');
        option.value = column;
        option.textContent = column;
        indexSelector.appendChild(option.cloneNode(true));
        targetSelector.appendChild(option);
    });

    document.getElementById('column-selector').style.display = 'block';
    document.getElementById('target-selector').style.display = 'block';
}

function setIndexAndTarget() {
    let indexColumn = document.getElementById('index-column-list').value;
    let targetColumn = document.getElementById('target-column-list').value;

    fetch('/set_columns', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            index_column: indexColumn, 
            target_column: targetColumn 
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data && data.error) {
            console.error('Error:', data.error);
            showMessage(data.error, 'error');
        } else {
            console.log('Columns set successfully:', data);
            showMessage('Index and target columns set successfully.', 'success');
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        showMessage(`Fetch error: ${error.message}`, 'error');
    });
}

function showMessage(message, type) {
    let messageBox = document.getElementById('message-box');
    messageBox.textContent = message;
    messageBox.className = type;
    messageBox.style.display = 'block';
}
