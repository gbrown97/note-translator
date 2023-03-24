from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def printTest():
    return "Note Translator"

userDB = {}     #for testing ...need to replace

@app.route('/display', methods=['POST'])
def display():          #for testing only...remove later
    for user in userDB:
        print(user + "\t" + userDB[user]) 
    return jsonify({'message': 'Users displayed'}), 201

@app.route('/signup', methods=['POST'])
def signUp():
    userName = request.json.get('username')
    password = request.json.get('pwd')

    if userName in userDB:
        return jsonify({'error': 'Username already exists'}), 400
    userDB[userName] = password

    return jsonify({'message': 'User created'}), 201


@app.route('/login', methods=['POST'])
def logIn():
    userName = request.json.get('username')
    password = request.json.get('pwd')

    if userName not in userDB or userDB[userName] != password:
        return jsonify({'error': 'Invalid username/password'}), 401
    

    return jsonify({'message': 'Login successful'}), 200


@app.route('/upload', methods=['POST'])
def uploadNotes():
    
    return jsonify({'message': 'Notes upload successful'}), 200

@app.route('/list', methods=['POST'])
def listNotes():
    
    return jsonify({'message': 'Notes listed'}), 200

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
