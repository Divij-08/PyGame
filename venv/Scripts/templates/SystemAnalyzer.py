UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
ALLOWED_EXTENSIONS = {'html'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_file(os.path.join(app.config['UPLOAD_FOLDER'],filename),filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')
import pandas as pd
from openpyxl import load_workbook

DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
def process_file(path, filename):
   Convert_Excel(path, filename)
def Convert_Excel(path,filename):
    df = pd.read_html(path)
    # df[0].to_csv('data.csv')
    shared_df = df[0][df[0]['Usage'] == 'shared']
    shared_df = shared_df[['Variables','Tasks (Write)','Tasks (Read)','Detailed Type','Nb Read','Nb Write']]
    shared_df.rename(columns={"Tasks (Write)": "W.T","Tasks (Read)": "R.T",},inplace=True)
    shared_df.to_excel('data.xlsx',index=False)

    workbook = load_workbook('data.xlsx')
    sheet = workbook.active
    length = len(sheet['A'])
    for i in range(2, length+1):
        ch = 'A' + str(i)
        sheet[ch] = sheet[ch].value.split('.')[-1]
    output_stream = open(app.config['DOWNLOAD_FOLDER'],+ filename, 'wb')
    output.write(output_stream)

@app.route('/uploads/<filename>')
def uploaded_file(filename='data.xlsx'):
   return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
