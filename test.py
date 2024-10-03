import subprocess
import os

output_dir = 'outputs/ApluSeLetter/output'
tex_file = 'outputs/ApluSeLetter/output/ApluSeoutput.tex'

os.makedirs(output_dir, exist_ok=True)

try:
    subprocess.run(['pdflatex', '-output-directory=' + output_dir, tex_file], check=True)
except subprocess.CalledProcessError as e:
    print(f'Error occurred: {e}')