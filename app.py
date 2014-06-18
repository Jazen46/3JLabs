import os.path
import db
from flask import Flask, redirect, request, render_template, url_for, send_from_directory, session
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key="dsjhgaslkdjfd"
app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt','mp3','bmp','jpg','jpeg'])
@app.route('/')
def index():
    if "username" in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard.html',uploads = db.getUploads(session['username']))
    else:
        return redirect(url_for('index'))

@app.route("/signup",methods=['GET',"POST"])
def signup():
    if request.method=='POST':
        if request.form.get("password","")==request.form.get("password2",""):
            result=db.createUser(request.form.get("username").lower(),request.form.get('password'))
            if result==0:
                session['username']=request.form.get('username')
            return redirect(url_for('index'))

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=="POST":
        result = db.authorize(str(request.form.get("username")).lower(),str(request.form.get("password")));
        if result==0:
            session["username"]=request.form.get("username");
        return redirect(url_for("index"))          

@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for('index'))
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
            createDirectory(app.config['UPLOAD_FOLDER'] + session['username'] + "/"+ package)
            filename=secure_filename(file.filename)
            summary=str(request.form.get("summary"))
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+session['username']+'/'+ package,filename))
            #music=secure_filename(mp3.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER']+package,music))
            uploadinfo = {'Creator':session['username'],
                'Package':package,
                'Main':filename,
                'Summary':summary};
            db.addUpload(session['username'],uploadinfo)
            return redirect(url_for("dashboard"))
            #return redirect(url_for('uploaded_file',username=session['username'],package=package,filename=filename))
    return render_template('upload.html')

@app.route('/uploads/<username>/')
def user(username):
    uploads = db.getUploads(username)
    return render_template("user.html",uploads=uploads)


@app.route('/uploads/<username>/<package>/<filename>')
def uploaded_file(username,package,filename):
    return send_from_directory(app.config['UPLOAD_FOLDER']+username+"/"+package,filename)

@app.route('/uploads/<username>/<package>/')
def uploaded_package(username,package):
    uploads = db.getUploads(username)
    package=[upload for upload in uploads if upload["Package"]==package][0]
    return render_template("package.html",package=package)

@app.route('/delete/<int:id>', methods=['POST'])
def remove(id):
    """Delete an uploaded file."""
    upload = Upload.query.get_or_404(id)
    delete(upload)
    return redirect(url_for('index'))
        
    
if __name__ == "__main__":
    app.run(debug=True)
