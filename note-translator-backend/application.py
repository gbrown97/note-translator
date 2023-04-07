from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow    #for serializing json data---remove?
from flask_cors import CORS
from util import S3Storage
from noteTranslate import NoteTranslator
import pathlib
import os

basedir = pathlib.Path(__file__).parent.resolve()

application = app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{basedir / 'user.db'}" #'sqlite:///user.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'jpg'}
app.config['USERNAME'] = ''
CORS(app)
db = SQLAlchemy(app) # new
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(32))
    password = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    lname = db.Column(db.String(32))
    setLang = db.Column(db.String(32))

    def __repr__(self):
        return '<USERS %s>' % self.title

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id","email", "username", "password",'fname','lname','setLang')
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/")
def printTest():
    return "Note Translator"

@app.route('/display', methods=['POST'])
def display():          #for testing only...remove later
    people = User.query.all()
    return users_schema.dump(people) 
    #return jsonify({'message': 'Users displayed'}), 201

@app.route('/signup', methods=['POST'])
def signUp():
    new_user = User(
            username=request.json['username'],
            password=request.json['password'],
            fname=request.json['fname'],
            lname=request.json['lname'],
            setLang=request.json['setLang'],
            email=""
        )
   
    existing_user = User.query.filter(User.username == new_user.username).one_or_none()
    if existing_user is None:
        db.session.add(new_user)
        db.session.commit()
        sobj = S3Storage(request.json['username'])
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"Person already exists")


@app.route('/login', methods=['POST'])
def logIn():
    #userName = request.json.get('username')
    #password = request.json.get('pwd')
    user = User(
            username=request.json['username'],
            password=request.json['password']
        )
    existing_user = User.query.filter_by(username=user.username).first()
    if not existing_user or existing_user.password!=user.password:
        return jsonify({'error': 'Invalid username/password'}), 401
    
    app.config['USERNAME'] = request.json['username']
    sobj = S3Storage(request.json['username'])
    print(app.config['USERNAME'])
    return jsonify({'message': 'Login successful'}), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']   

@app.route('/upload', methods=['POST'])
def uploadNotes():
    print(request.files)
    if 'file' not in request.files:
       return jsonify({'error': 'No file selected.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File is empty.'}), 400
    #username= app.config['USERNAME']
    #print(app.config['USERNAME'])
    username=request.form['username']
    contents=file.read()
    sobj = S3Storage(username)
    sobj.uploadTxt(contents,file.filename)
    return jsonify({'message': 'Notes upload successful'}), 200

@app.route('/list', methods=['POST'])
def listNotes():
   username=request.json['username']
   #username= app.config['USERNAME']
   #print(app.config['USERNAME'])
   sobj = S3Storage(username)
   #userName = request.json.get('username')
   #sobj=S3Storage(request.json.get('username'))
   files = sobj.listFiles()
   fileslist= []
   for i in range(len(files)):
       if files[i].startswith(username + "/") and files[i] != username+"/":
           fileslist.append(files[i][len(username + "/"):])
                  
   return jsonify({"files": fileslist})

@app.route('/send',methods=['POST'])
def sendUserDetails():
    user = User(
            username=request.json['username']
        )
    existinguser = User.query.filter_by(username=user.username).first()
    if existinguser:
        userDetails= (existinguser.username,
                  existinguser.fname,
                  existinguser.lname,
                  existinguser.setLang)
        return jsonify({"userDetails": userDetails})
    return jsonify({'message': 'User does not exist'}), 400

@app.route('/users',methods=['POST'])
def sendUsers():
    users = User.query.all()
    userlist=[]
    #usernames = [user.username for user in users]
    for user in users:
        userdict = {
            'username':user.username,
            'name':user.fname +" "+user.lname,
            'setLang':user.setLang
        }
        userlist.append(userdict)
    return jsonify(userlist)

@app.route('/share', methods=['POST'])
def shareNotes():
    sendername=request.json['username']
    #sendername= app.config['USERNAME']
    receivername= request.json['recName']
    print(sendername+ " "+receivername )
    sender = User.query.filter_by(username=sendername).first()
    srcLang=sender.setLang
    receiver = User.query.filter_by(username=receivername).first()
    destLang=receiver.setLang
    #if 'file' not in request.files:
     #  return jsonify({'error': 'No file selected.'}), 400
    #file = request.files['file']
    file=request.json['file']
    if not file:
        return jsonify({'error': 'No file selected.'}), 400
    sobj = S3Storage(sendername)
    objectTrans =  NoteTranslator(srcLang,file,sobj)
    transContent=objectTrans.translate(destLang,sendername)
    sobj = S3Storage(receivername)
    if file.endswith(".txt"):
        sobj.uploadTxt(transContent, file)
    else:
        filename = file.split(".")[0] + ".txt"
        print(filename)
        sobj.uploadTxt(transContent, filename) 
    return jsonify({'message': 'Notes shared successful'}), 200

@app.route('/delete', methods=['POST'])
def deleteNotes():
    sobj=S3Storage(request.json['username'])
    sobj.deleteFile(request.json['file'])
    return jsonify({'message': 'Notes deleted successful'}), 200

@app.route('/translate', methods=['POST']) #explicit translate
def translateNotes():
    sendername=request.json['username']
    #sendername= app.config['USERNAME']
    existing_user = User.query.filter_by(username=sendername).first()
    srcLang=existing_user.setLang
    #print(app.config['USERNAME'])
    file=request.json['file']
    #if 'file' not in request.files:
     #  return jsonify({'error': 'No file selected.'}), 400
    #file = request.files['file']
    sobj = S3Storage(sendername)
    srcLang = request.json['srcLang']
    objectTrans =  NoteTranslator(srcLang,file,sobj)
    destLang= request.json['destLang']
    transContent=objectTrans.translate(destLang,sendername)
    sobj = S3Storage(sendername)
    if file.endswith(".txt"):
        sobj.uploadTxt(transContent, file)
    else:
        filename = file.split(".")[0] + ".txt"
        print(filename)
        sobj.uploadTxt(transContent, filename)    
    return jsonify({'message': 'Notes translated successful'}), 200

@app.route('/view', methods=['POST'])
def viewFile():
    username=request.json['username']
    #username= app.config['USERNAME']
    #file = request.files['file']
    file=request.json['file']
    user = User.query.filter_by(username=username).first()
    sobj = S3Storage(username)
    srcLang=user.setLang
    objectFile = NoteTranslator(srcLang,file,sobj)
    fileContents = objectFile.readFile(username)
    print(fileContents)
    return fileContents

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
