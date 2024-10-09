function collectEditorData() {
    const editor = document.getElementById('editor');
    const editorContent = editor.innerHTML; // Получаем HTML-код из редактора
    // const editorText = editor.innerText; // Получаем текст из редактора (без HTML-тегов)

    // Пример: Отправка данных на сервер или дальнейшая обработка
    console.log("Содержимое редактора:", editorContent);

    // Отправка данных через WebSocket (если вы используете его)
    socket.emit('update_editor_content', { content: editorContent });

    // Вы также можете сохранить данные в localStorage, если это необходимо
    localStorage.setItem('editorContent', editorContent);
}

const socket = io();
const editor = document.getElementById('editor');

// Функция для автоматического изменения размера редактора
function autoResize() {
    editor.style.height = 'auto'; // Сначала сбрасываем высоту
    editor.style.height = editor.scrollHeight + 'px'; // Устанавливаем новую высоту
}

// Функция для применения команды форматирования
function execCommand(command) {
    document.execCommand(command, false, null);
    autoResize(); // Обновляем размер после применения команды
}

// Первоначальный вызов для установки высоты при загрузке страницы
autoResize();

// Функция для загрузки данных из localStorage
function loadData() {
    const fields = ['about', 'object', 'address', 'whom', 'dear', 'senderNS', 'senderSt'];

    fields.forEach(field => {
        const value = localStorage.getItem(field);
        // if (value) {
        document.getElementById(field).value = value; // Заполняем поле данными
    });

    const formData = {};

    fields.forEach(field => {
        formData[field] = document.getElementById(field).value;
    });
    socket.emit('update_data_apluseletter', formData);
}

// Функция отправки данных на сервер при каждом изменении
function sendData() {
    const fields = ['about', 'object', 'address', 'whom', 'dear', 'senderNS', 'senderSt'];
    const formData = {};

    fields.forEach(field => {
        formData[field] = document.getElementById(field).value;
        const value = formData[field];
        localStorage.setItem(field, value); // Сохраняем данные в localStorage
    });

    // Отправляем данные на сервер через WebSocket
    socket.emit('update_data_apluseletter', formData);
}

// Получение обновленного PDF и отображение в object
socket.on('update_pdf', function(data) {
    if (data.error) {
        console.error('Error generating PDF:', data.error);
    } else {
        // Преобразуем строку обратно в бинарный PDF файл
        const pdfBlob = new Blob([new Uint8Array(data.pdf_data.split('').map(char => char.charCodeAt(0)))], { type: 'application/pdf' });
        const pdfUrl = URL.createObjectURL(pdfBlob);
        document.getElementById('pdfPreview').data = pdfUrl;
    }
});

function clearStorage() {
    localStorage.clear();
    loadData();
    alert('Очищено!');
}

window.onload = loadData;