from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow    #for serializing json data---remove?
from flask_cors import CORS
import pathlib

basedir = pathlib.Path(__file__).parent.resolve()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{basedir / 'user.db'}" #'sqlite:///user.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
            fname=request.json['fName'],
            lname=request.json['lName'],
            setLang=request.json['selLang'],
        )
   
    existing_user = User.query.filter(User.username == new_user.username).one_or_none()
    if existing_user is None:
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"Person already exists")


@app.route('/login', methods=['POST'])
def logIn():
    #userName = request.json.get('username')
    #password = request.json.get('pwd')
    user = User(
            email=request.json['email'],
            pwd=request.json['password']
        )
    existing_user = User.query.filter_by(email=user.email).first()
    if not existing_user or existing_user.pwd!=user.pwd:
        return jsonify({'error': 'Invalid username/password'}), 401
    

    return jsonify({'message': 'Login successful'}), 200


@app.route('/upload', methods=['POST'])
def uploadNotes():

    return jsonify({'message': 'Notes upload successful'}), 200

@app.route('/list', methods=['POST'])
def listNotes():
   
   return jsonify({'message': 'Notes listed'}), 200
   ''' userName = request.json.get('username') #get username
    sobj = S3Storage('username')
    if userName not in userDB :
        return jsonify({'error': 'User doesnt exist'}), 401
    print(sobj.listFiles())
    '''
   

@app.route('/share', methods=['POST'])
def shareNotes():
    
    return jsonify({'message': 'Notes shared successful'}), 200

@app.route('/delete', methods=['POST'])
def deleteNotes():
    
    return jsonify({'message': 'Notes deleted successful'}), 200

@app.route('/translateNotes', methods=['POST'])
def translateNotes():
    
    return jsonify({'message': 'Notes translated successful'}), 200


if __name__ == '__main__':
    app.run(debug=True)
