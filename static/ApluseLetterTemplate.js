const socket = io();
const editor = document.getElementById('body');

function collectEditorData() {
    const editorContent = editor.innerHTML;
    socket.emit('update_editor_content', { content: editorContent });
    // alert(editorContent);
    localStorage.setItem('body', editorContent);
}

function autoResize() {
    editor.style.height = 'auto';
    editor.style.height = editor.scrollHeight + 'px';
}

function execCommand(command) {
    document.execCommand(command, false, null);
    autoResize();
}

autoResize();

function loadData() {
    const fields = ['about', 'object', 'address', 'whom', 'dear', 'senderNS', 'senderSt'];

    document.getElementById('body').innerHTML = localStorage.getItem('body');

    fields.forEach(field => {
        const value = localStorage.getItem(field);
        document.getElementById(field).value = value;
    });

    const formData = {};

    fields.forEach(field => {
        formData[field] = document.getElementById(field).value;
    });
    socket.emit('update_data_apluseletter', formData);
}

function sendData() {
    const fields = ['about', 'object', 'address', 'whom', 'dear', 'senderNS', 'senderSt'];
    const formData = {};
    formData['body'] = editor.innerHTML;
    localStorage.setItem('body', editor.innerHTML);

    fields.forEach(field => {
        formData[field] = document.getElementById(field).value;
        const value = formData[field];
        localStorage.setItem(field, value);
    });


    socket.emit('update_data_apluseletter', formData);
}

socket.on('update_pdf', function(data) {
    if (data.error) {
        console.error('Error generating PDF:', data.error);
    } else {
        const pdfBlob = new Blob([new Uint8Array(data.pdf_data.split('').map(char => char.charCodeAt(0)))], { type: 'application/pdf' });
        const pdfUrl = URL.createObjectURL(pdfBlob);
        document.getElementById('pdfPreview').data = pdfUrl;
    }
});

function clearStorage() {
    // Запрос подтверждения у пользователя
    if (confirm('Вы уверены, что хотите очистить все данные?')) {
        localStorage.clear(); // Очищаем localStorage
        loadData(); // Загружаем данные заново
    }
}

window.onload = function() {
    loadData();
    autoResize();
};