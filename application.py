import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = str(request.form.get("inputUsername"))
        print("username: " + username)

        return username

    return render_template("index.html")
