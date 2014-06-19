import os
from flask import Flask, request, redirect, url_for, render_template
from flask.ext.pymongo import PyMongo


app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return mongo.send_file(filename)

#data is the file being uploaded
#@app.route('/uploads/<path:filename>',methods=['POST'])
def save_file(filename, file):
    mongo.save_file(filename, file)
    
    

@app.route('/', methods=['POST','GET'])
def upload_file():

    if request.method =="POST":
        print "got here"
        filename = request.form.get("title","")
        print "sofarsogood"
        file = request.files['file']
        print"still good"
        save_file(filename,file)
        print "huh, still good"
        print filename
        return redirect("/uploads/" + filename)
    else:
        return render_template("upload.html")
        
    
if __name__ == "__main__":
    app.run(debug=True)
