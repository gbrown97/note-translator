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
    print("YAY")
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
    #app.config['sobj'] = sobj
    print(app.config['USERNAME'])
    return jsonify({'message': 'Login successful'}), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']   

@app.route('/upload', methods=['POST'])
def uploadNotes():
    #print(request)
    #print("uploadtest")
    print(request.files)
    if 'file' not in request.files:
       return jsonify({'error': 'No file selected.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File is empty.'}), 400
    username= app.config['USERNAME']
    print(app.config['USERNAME'])
    contents=file.read()
    sobj = S3Storage(username)
    sobj.uploadTxt(contents,file.filename)

    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return jsonify({'message': 'Notes upload successful'}), 200

@app.route('/list', methods=['POST'])
def listNotes():
   username= app.config['USERNAME']
   print(app.config['USERNAME'])
   sobj = S3Storage(username)
   #userName = request.json.get('username')
   #sobj=S3Storage(request.json.get('username'))
   files = sobj.listFiles()
   #files = os.listdir(app.config['UPLOAD_FOLDER'])
   print(files)
   return jsonify({"files": files})
   '''return jsonify({'message': 'Notes listed'}), 200
    userName = request.json.get('username') #get username
    sobj = S3Storage('username')
    if userName not in userDB :
        return jsonify({'error': 'User doesnt exist'}), 401
    print(sobj.listFiles())
    '''
   

@app.route('/share', methods=['POST'])
def shareNotes():
    sendername= app.config['USERNAME']
    receivername= request.form['recName']
    sender = User.query.filter_by(username=sendername).first()
    srcLang=sender.setLang
    receiver = User.query.filter_by(username=receivername).first()
    destLang=receiver.setLang
    if 'file' not in request.files:
       return jsonify({'error': 'No file selected.'}), 400
    file = request.files['file']
    sobj = S3Storage(sendername)
    objectTrans =  NoteTranslator(srcLang,file.filename,sobj)
    transContent=objectTrans.translate(destLang)
    sobj = S3Storage(receivername)
    sobj.uploadTxt(transContent, file.filename)
    return jsonify({'message': 'Notes shared successful'}), 200

@app.route('/delete', methods=['POST'])
def deleteNotes():
    sobj=S3Storage(request.json.get('username'))
    sobj.deleteFile(request.json.get('file'))
    return jsonify({'message': 'Notes deleted successful'}), 200

@app.route('/translate', methods=['POST']) #explicit translate
def translateNotes():
    sendername= app.config['USERNAME']
    existing_user = User.query.filter_by(username=sendername).first()
    srcLang=existing_user.setLang
    #print(app.config['USERNAME'])
    if 'file' not in request.files:
       return jsonify({'error': 'No file selected.'}), 400
    file = request.files['file']
    sobj = S3Storage(sendername)
    srcLang = request.form['srcLang']
    objectTrans =  NoteTranslator(srcLang,file.filename,sobj)
    destLang= request.form['destLang']
    transContent=objectTrans.translate(destLang)
    sobj = S3Storage(sendername)
    sobj.uploadTxt(transContent, file.filename)
    return jsonify({'message': 'Notes translated successful'}), 200


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
