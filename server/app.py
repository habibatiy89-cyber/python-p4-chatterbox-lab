#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Message

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return "Chatterbox API"


# -------------------- GET + POST --------------------
@app.route("/messages", methods=["GET", "POST"])
def messages():

    if request.method == "GET":
        messages = Message.query.order_by(Message.created_at.asc()).all()
        response = make_response(
            [m.to_dict() for m in messages],
            200
        )
        return response

    elif request.method == "POST":
        data = request.get_json()

        new_message = Message(
            body=data.get("body"),
            username=data.get("username")
        )

        db.session.add(new_message)
        db.session.commit()

        response = make_response(
            new_message.to_dict(),
            201
        )
        return response


# -------------------- PATCH + DELETE --------------------
@app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
def message_by_id(id):

    message = Message.query.filter(Message.id == id).first()

    if not message:
        return make_response(
            {"error": "Message not found"},
            404
        )

    if request.method == "PATCH":
        data = request.get_json()

        if "body" in data:
            message.body = data["body"]

        db.session.commit()

        return make_response(
            message.to_dict(),
            200
        )

    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        return make_response(
            {"delete_successful": True},
            200
        )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
