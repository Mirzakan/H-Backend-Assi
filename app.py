from flask import Flask, jsonify, request

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

users = [
    {
        'name': 'daniel',
        'sent': [],
        'inbox': {
            'read': [
                {
                    'sender' : 'yael hanim',
                    'reciver' : 'daniel',
                    'message' : 'Hi, Welcome aboard!',
                    'subject' : 'New Employee',
                    'creation date' : '20/01/2021',
                },
            ],
            'unread': [
                {
                    'sender' : 'gilad aharon',
                    'reciver' : 'daniel',
                    'message' : 'you will support the next sprint',
                    'subject' : 'New Sprint',
                    'creation date' : '30/01/2021',
                },
                {
                    'sender' : 'ilan paul',
                    'reciver' : 'daniel',
                    'message' : 'Hello Team! please check your open bugs',
                    'subject' : 'Build',
                    'creation date' : '02/02/2021',
                },
            ]
        },
    },
    {
        'name': 'gabriel',
        'sent': [],
        'inbox': {
            'read': [
                {
                    'sender' : 'haim yakir',
                    'reciver' : 'daniel',
                    'subject' : 'New Employee',
                    'message' : 'Welcome',
                    'creation date' : '25/01/2021',
                },
            ],
            'unread': []
        },
    },
]

@app.route('/')
def home():
    return 'User Messages API'

@app.route("/users/all", methods=["GET"])
def getUsers():
    return jsonify(users)

@app.route('/users/<string:name>/compose', methods=['POST'])
def composeMessage(name):
    request_data = request.get_json()
    for user in users:
        if(user['name'] == name):
            new_message = {
                'sender': request_data['sender'],
                'reciver': request_data['reciver'],
                'subject': request_data['subject'],
                'message': request_data['message'],
                'creation date': request_data['creation date']
            }
            user['inbox']['unread'].append(new_message)
            return '<h3> Message sent: </h3> {0} '.format(new_message['message'])
    return jsonify({'message':'store not found'})

@app.route("/users/<string:name>/inbox", methods=["GET"])
def getAllUserMessages(name):
    for user in users:
        if(user['name'] == name):
            return jsonify(user['inbox'])
    return jsonify({'message':'user not found'})

@app.route("/users/<string:name>/inbox/unread/all", methods=["GET"])
def getUnreadUserMessages(name):
    for user in users:
        if(user['name'] == name):
            return jsonify(user['inbox']['unread'])
    return jsonify({'message':'message not found'})

@app.route("/users/<string:name>/inbox/read/all", methods=["GET"])
def getReadUserMessages(name):
    for user in users:
        if(user['name'] == name):
            return jsonify(user['inbox']['read'])
    return jsonify({'message':'message not found'})

@app.route("/users/<string:name>/inbox/read", methods=["GET"])
def readMessage(name):
    for user in users:
        if(user['name'] == name):
            inbox = user['inbox']['unread']
            if(len(inbox) > 0):
                message = inbox.pop(0)
                user['inbox']['read'].append(message)
                return jsonify(message)
            else:
                return '<h3>No New Messages</h3>'
    return jsonify({'message':'message not found'})

@app.route("/users/<string:name>/inbox/read/delete", methods=["GET"])
def deleteReadMessage(name):
    for user in users:
        if(user['name'] == name):
            inbox = user['inbox']['read']
            if(len(inbox) > 0):
                message = inbox.pop(0)
                return '{0} </br> <h3> Message deleted </h3>'.format(message['message'])
        return '<h3>No Messages</h3>'
    return jsonify({'message':'message not found'})

@app.route("/users/<string:name>/inbox/unread/delete", methods=["GET"])
def deleteUnreadMessage(name):
    for user in users:
        if(user['name'] == name):
            inbox = user['inbox']['unread']
            if(len(inbox) > 0):
                message = inbox.pop(0)
                return '<h3> Message have been deleted: </h3> {0}'.format(message['message'])
        return '<h3>No Messages</h3>'
    return jsonify({'message':'message not found'})

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.run()