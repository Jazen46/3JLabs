import os.path
from flask import Flask, redirect, request, render_template, url_for, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.storage import Storage
from flask.ext.uploads import delete, init, save, Upload
from werkzeug import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt','mp3','bmp','jpg','jpeg'])
@app.route('/')
def index():
    """List the uploads."""
    uploads = Upload.query.all()
    return (
        '<a href="/upload">New Upload</a><br>' +
        u''.join(
            u'<a href="%s">%s</a>'
            u'<form action="/delete/%s" method="POST">'
            u' <button type="submit">Delete</button>'
            u'</form><br>'
            % (Storage().url(u.name), u.name, u.id)
            for u in uploads
        )
    )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']
def allowed_music(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']
def getExtension(filename):
    return '.'+filename.rsplit('.',1)[1]

def createDirectory(dirName):
    os.getcwd()
    print(dirName)
    if not os.path.exists(dirName):
        os.makedirs(dirName)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a new file."""
    if request.method == 'POST':
        file = request.files['main']
        mp3 = request.files['music']
        if file and allowed_file(file.filename):# and mp3 and allowed_music(mp3.filename):
            package=str(request.form.get("package",""))
            createDirectory(app.config['UPLOAD_FOLDER'] + package)
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+package,filename))
            #music=secure_filename(mp3.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER']+package,music))
            return redirect(url_for('uploaded_file',package=package,filename=filename))
    return render_template('upload.html')

@app.route('/uploads/<package>/')
def package(package):
    return os.listdir()


@app.route('/uploads/<package>/<filename>')
def uploaded_file(package,filename):
    return send_from_directory(app.config['UPLOAD_FOLDER']+package,filename)
@app.route('/delete/<int:id>', methods=['POST'])
def remove(id):
    """Delete an uploaded file."""
    upload = Upload.query.get_or_404(id)
    delete(upload)
    return redirect(url_for('index'))
        
    
if __name__ == "__main__":
    app.run(debug=True)
