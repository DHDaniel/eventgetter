from flask import Flask, session, request, render_template, redirect, url_for
import dateutil.parser
import requests
import os
import json
import datetime
import pprint

app = Flask(__name__)

app.config.from_envvar("APP_SETTINGS")

def get_user_info(token):
    headers = {"Authorization": "Bearer {}".format(token)}
    r = requests.get("https://www.eventbriteapi.com/v3/users/me/", headers=headers)
    resp = r.json()
    return resp

def get_events(token):
    headers = {"Authorization": "Bearer {}".format(token)}
    r = requests.get("https://www.eventbriteapi.com/v3/users/me/events/", headers=headers)
    resp = r.json()
    parsed_events = []
    for event in resp['events']:
        parsed_obj = dateutil.parser.parse(event['start']['local'])
        parsed_date = parsed_obj.strftime('%B %d, %Y')
        parsed_time = parsed_obj.strftime('%I:%M %p')
        parsed_tz = event['start']['timezone'].replace("_", " ")
        event['start_time_local'] = parsed_time
        event['start_date_local'] = parsed_date
        event['start_tz'] = parsed_tz
        parsed_events.append(event)
    resp['events'] = parsed_events
    return resp

@app.route('/')
def index():

    if "eventbrite_token" in session:
        user_info = get_user_info(session['eventbrite_token'])
        events = get_events(session['eventbrite_token'])
        #pprint.pprint(events['events'])
        return render_template('events_list.html', events=events['events'], user_info=user_info)
    else:
        return redirect(url_for('login'))


@app.route('/login')
def login():
    access_code = request.args.get("code", default=None)
    if access_code:
        EVENTBRITE_SECRET = os.environ.get("EVENTBRITE_SECRET")
        EVENTBRITE_APP_KEY = os.environ.get("EVENTBRITE_APP_KEY")
        data = {"code": access_code,
                "client_secret": EVENTBRITE_SECRET,
                "client_id": EVENTBRITE_APP_KEY,
                "grant_type": "authorization_code"}
        r = requests.post("https://www.eventbrite.com/oauth/token", data=data)
        response = r.json()
        session['eventbrite_token'] = response['access_token']
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('eventbrite_token', None)
    return redirect(url_for('index'))
