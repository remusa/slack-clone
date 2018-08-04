import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_session import Session
from flask_socketio import SocketIO, emit
from collections import defaultdict

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user"):
        return redirect(url_for("channels"))

    if request.method == "POST":
        username = str(request.form.get("inputUsername"))
        session["user"] = username
        return redirect(url_for("channels"))

    return render_template("index.html", channels_list=channels_list)


@app.route("/channels", methods=["GET", "POST"])
def channels():
    if not session.get("user"):
        flash("Log in to view channels")
        return redirect(url_for("index"))
    else:
        username = session.get("user")

    # print(channels_list)

    if request.method == "POST":
        channel = str(request.form.get("inputChannel"))

        if any(channel in s for s in channels_list):
            flash("Channel already exists")
        else:
            channels_list.append(channel)

    # flash("Welcome, " + session.get("user"))
    return render_template("channels.html", username=username, channels_list=channels_list)


channels_list = []

messages_dictionary = {
    "channel3": [{
        "username": ["user1", "user2"],
        "messages": ["hello", "hello"]
    }]
}

usernames_list = []
messages_list = []

MAX_MESSAGES = 5


@app.route("/channel/<string:channel>", methods=["GET", "POST"])
def channel(channel):
    username = session.get("user")
    chat_list = []

    # if current channel exists
    if any(channel in s for s in channels_list):
        messages_list = messages_dictionary
    # new channel
    # else:

    if request.method == "POST":
        inputMessage = str(request.form.get("inputMessage"))
        usernames_list.append(username)
        messages_list.append(inputMessage)

        chat_list = []
        if len(usernames_list) > MAX_MESSAGES or len(messages_list) > MAX_MESSAGES:
            usernames_list.pop(0)
            messages_list.pop(0)

        for user, message in zip(usernames_list, messages_list):
            chat_list.append([user, message])
        #     chat_dictionary[user] = message

    return render_template("channel.html", channel=channel, username=username, chat_list=chat_list)


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Successfully logged out")
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
