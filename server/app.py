from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '''<h1>Welcome to Chatterbox!! (but I don't actually say much...)'''

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        return make_response( [message.to_dict() for message in Message.query.order_by(Message.created_at).all()], 200 )
        # msg_list = []
        # for msg in Message.query.order_by(Message.created_at).all:
        #     breakpoint()

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data["body"],
            username=data["username"]
        )

        db.session.add(new_message)
        db.session.commit()

        msg_dict = new_message.to_dict()

        return make_response( msg_dict, 200)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    msg = Message.query.filter_by(id=id).first()

    if msg == None:
        response_body = {"message": "No message of that sort here...Please try again."}
        return make_response( response_body, 404)
    else:

        if request.method == 'PATCH':
            for attr in request.get_json():
                setattr(msg, attr, request.get_json().get(attr))
            db.session.add(msg)
            db.session.commit()
            msg_dict = msg.to_dict()
            return make_response( msg_dict, 200 )

        elif request.method == 'DELETE':
            db.session.delete(msg)
            db.session.commit()
            response_body = {
                "Delete Successful!!": True,
                "Message": "Message deleted"
            }
            return make_response( response_body, 200 )

if __name__ == '__main__':
    app.run(port=5555)
