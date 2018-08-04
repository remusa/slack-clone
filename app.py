import os
import requests
import datetime
import time

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


MAX_MESSAGES = 100
channels_dictionary = {"testchannel": ["user1: this is a message"]}


@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user"):
        return redirect(url_for("channels"))

    if request.method == "POST":
        username = str(request.form.get("inputUsername"))
        session["user"] = username
        return redirect(url_for("channels"))

    return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Successfully logged out")
    return redirect(url_for("index"))


@app.route("/channels", methods=["GET", "POST"])
def channels():
    if not session.get("user"):
        flash("Log in to view channels")
        return redirect(url_for("index"))
    else:
        username = session.get("user")

    for key, value in channels_dictionary.items():
        print(key, value)

    if request.method == "POST":
        channel = str(request.form.get("inputChannel"))

        if channel in channels_dictionary:
            flash("Channel already exists")
        else:
            flash("New channel created")
            channels_dictionary[channel] = []

    return render_template(
        "channels.html", username=username, channels_dictionary=channels_dictionary
    )


@app.route("/channel/<string:channel>")
def channel(channel):
    if not session.get("user"):
        flash("Log in to view channels")
        return redirect(url_for("index"))
    else:
        username = session.get("user")

    return render_template(
        "channel.html",
        username=username,
        channel=channel,
        messages_list=channels_dictionary.get(channel),
    )


@socketio.on("submit message")
def submit(data):
    username = session.get("user")
    inputMessage = data["message"]
    current_channel = data["channel"]

    timestamp = time.gmtime()
    readable = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    print("readable: " + readable)

    new_message = "[" + readable + "]\t" + username + ": " + inputMessage

    channel_list = channels_dictionary.get(current_channel)

    channel_list.append(new_message)
    print(*channel_list, sep=", ")

    if len(channel_list) >= MAX_MESSAGES:
        channel_list.pop(0)

    emit("channel messages", new_message, broadcast=True)


if __name__ == "__main__":
    app.run(debug=True)
