from flask import Flask, session, request, render_template, redirect, url_for
import requests
import os
import json

app = Flask(__name__)

app.config.from_envvar("APP_SETTINGS")

@app.route('/')
def index():
    print(request.args)
    if "eventbrite_token" in session:
        return render_template('events_list.html')
    else:
        return redirect(url_for('login'))


@app.route('/login')
def login():
    print(request.args)
    if "access_token" in request.args:
        EVENTBRITE_SECRET = os.environ.get("EVENTBRITE_SECRET")
        EVENTBRITE_APP_KEY = os.environ.get("EVENTBRITE_APP_KEY")
        data = {code: request.args["access_token"],
                client_secret: EVENTBRITE_SECRET,
                client_id: EVENTBRITE_APP_KEY,
                grant_type: "authorization_code"}
        r = requests.post("https://www.eventbrite.com/oauth/token", data=data)
        response = r.json()
        print(response)
    else:
        return render_template('login.html')
