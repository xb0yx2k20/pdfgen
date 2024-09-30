import subprocess
import os
from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/nrpla')
def index_nrpla():
    return render_template('nrpla.html', pdfsrc='/static/output.pdf')

# Обработчик для получения данных через WebSocket
@socketio.on('update_data_nrpla')
def handle_update_data_nrpla(data):
    # Настройки Jinja2
    template_dir = 'templates/buketic'
    env = Environment(loader=FileSystemLoader(template_dir))

    city = data.get('city')
    date = data.get('date')
    landlordName = data.get('landlordName')
    num = data.get('num')
    baseWork = data.get('baseWork')
    landlordUserName = data.get('landlordUserName')
    renterName = data.get('renterName')
    renterUserName = data.get('renterUserName')
    base1Work = data.get('base1Work')
    areaNonRes = data.get('areaNonRes')
    areaMall = data.get('areaMall')
    address = data.get('address')
    price = data.get('price')
    deadline = data.get('deadline')

    # Рендеринг шаблона, настройка Jinja2
    template_file = 'NRPLAtemplate.tex'
    template = env.get_template(template_file)

    rendered_tex = template.render(price=price, deadline=deadline, city=city, date=date, landlordName=landlordName, num=num, baseWork=baseWork, landlordUserName=landlordUserName, renterName=renterName, renterUserName=renterUserName, base1Work=base1Work, areaNonRes=areaNonRes, areaMall=areaMall, address=address)

    # Сохранение отрендеренного шаблона в файл
    tex_file_path = 'templates/buketic/output/NRPLAoutput.tex'
    pdf_file_path = 'NRPLAoutput.pdf'
    
    with open(tex_file_path, 'w', encoding='utf-8') as f:
        f.write(rendered_tex)

    # Компиляция .tex файла в PDF с использованием pdflatex
    try:
        # os.chdir("templates/buketic/output")
        subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file_path], check=True)
        # os.chdir("../../../")

        # Отправляем PDF обратно клиенту для обновления превью
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        emit('update_pdf', {'pdf_data': pdf_data.decode('latin-1')})  # Кодируем PDF как строку для передачи


    except subprocess.CalledProcessError as e:
        print(f"Error during pdflatex compilation: {e}")
        emit('update_pdf', {'error': 'Error generating PDF'})


@app.route('/')
def index_letter():
    return render_template('test.html')

@app.route('/MgtuReport')
def index_MgtuReport():
    return render_template('MgtuReport.html')

# Маршрут для скачивания PDF
@app.route('/download_pdf')
def download_pdf():
    pdf_file_path = 'NRPLAoutput.pdf'
    return send_file(pdf_file_path, as_attachment=True)

# Функция для удаления временных файлов
def clean_up_files(file_list):
    for file_name in file_list:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"Removed file: {file_name}")
            except Exception as e:
                print(f"Error removing file {file_name}: {e}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)