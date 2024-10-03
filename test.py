import subprocess
import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='outputs/buketic')  # Указываем директорию для шаблонов

output_dir = 'templates/outputs/ApluSeLetter/output'
tex_file = 'templates/outputs/ApluSeLetter/output/ApluSeoutput.tex'

def render_and_save_template(template_file, output_tex_path, **template_vars):
    # Используем render_template для получения содержимого шаблона
    with app.app_context():  # Устанавливаем контекст приложения
        rendered_tex = render_template(template_file, **template_vars)

    with open(output_tex_path, 'w', encoding='utf-8') as f:
        f.write(rendered_tex)

template_file = 'NRPLAtemplate.tex'  # Указываем только имя файла
tex_file_path = 'templates/outputs/buketic/output/NRPLAoutput.tex'
pdf_file_path = 'templates/outputs/buketic/output/NRPLAoutput.pdf'
pdf_file_directory = 'templates/outputs/buketic/output'
data = {
    'city': 'Москва',
    'date': '03 октября 2024'
}
template_vars = {
    'city': 'kj',
    'date': "data.get('date')",
}

# Рендеринг и компиляция
render_and_save_template(template_file, tex_file_path, **template_vars)