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


@app.route('/a')
def index_a():
    return render_template('ApluseLetterTeamplate.html', pdfsrc='/static/output.pdf')


# Функция для рендеринга шаблона и сохранения в файл
def render_and_save_template(template_dir, template_file, output_tex_path, **template_vars):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)
    rendered_tex = template.render(**template_vars)

    with open(output_tex_path, 'w', encoding='utf-8') as f:
        f.write(rendered_tex)


# Функция для компиляции .tex файла в PDF
def compile_tex_to_pdf(tex_file_path):
    try:
        subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during pdflatex compilation: {e}")
        return False


# Функция для отправки PDF через WebSocket
def send_pdf_via_socket(output_pdf_path):
    try:
        with open(output_pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
        emit('update_pdf', {'pdf_data': pdf_data.decode('latin-1')})
    except Exception as e:
        print(f"Error sending PDF: {e}")
        emit('update_pdf', {'error': 'Error generating PDF'})


# Обработчик для NRPLA через WebSocket
@socketio.on('update_data_nrpla')
def handle_update_data_nrpla(data):
    # Данные для шаблона
    template_vars = {
        'city': data.get('city'),
        'date': data.get('date'),
        'landlordName': data.get('landlordName'),
        'num': data.get('num'),
        'baseWork': data.get('baseWork'),
        'landlordUserName': data.get('landlordUserName'),
        'renterName': data.get('renterName'),
        'renterUserName': data.get('renterUserName'),
        'base1Work': data.get('base1Work'),
        'areaNonRes': data.get('areaNonRes'),
        'areaMall': data.get('areaMall'),
        'address': data.get('address'),
        'price': data.get('price'),
        'deadline': data.get('deadline')
    }

    # Пути к файлам
    template_dir = 'templates/buketic'
    template_file = 'NRPLAtemplate.tex'
    tex_file_path = 'templates/buketic/output/NRPLAoutput.tex'
    pdf_file_path = 'NRPLAoutput.pdf'

    # Рендеринг и компиляция
    render_and_save_template(template_dir, template_file, tex_file_path, **template_vars)

    if compile_tex_to_pdf(tex_file_path):
        send_pdf_via_socket(pdf_file_path)
    else:
        emit('update_pdf', {'error': 'Error generating PDF'})


# Обработчик для ApluSeLetter через WebSocket
@socketio.on('update_data_apluseletter')
def handle_update_data_apluseletter(data):
    # Данные для шаблона
    template_vars = {
        'about': "\\textbf{" + data.get('about') + "}",
        'object': data.get('object'),  # Временно жестко зашитые данные
        'address': data.get('address'),
        'whom': data.get('whom')
    }


    # Пути к файлам
    template_dir = 'templates/ApluSeLetter'
    template_file = 'APLtemplate.tex'
    tex_file_path = 'templates/ApluSeLetter/output/ApluSeoutput.tex'
    pdf_file_path = 'ApluSeoutput.pdf'

    # Рендеринг и компиляция
    render_and_save_template(template_dir, template_file, tex_file_path, **template_vars)

    if compile_tex_to_pdf(tex_file_path):
        send_pdf_via_socket(pdf_file_path)
    else:
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