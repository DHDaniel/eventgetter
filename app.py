from flask import Flask, session, request, render_template, redirect, url_for
import dateutil.parser
import requests
import os
import json
import datetime

# initialize Flask app
app = Flask(__name__)

# get app settings from the config file, which includes the secret key for sessions
app.config.from_envvar("APP_SETTINGS")

def get_user_info(token):
    """
    Gets user information from Eventbrite

    Arguments:
    token -- the Eventbrite user OAuth token, used to authenticate with Eventbrite's API.

    Returns:
    resp -- the response from the API
    """
    # set token in request header
    headers = {"Authorization": "Bearer {}".format(token)}
    # hit API and parse response
    r = requests.get("https://www.eventbriteapi.com/v3/users/me/", headers=headers)
    resp = r.json()
    return resp

def get_events(token):
    """
    Gets user's events from Eventbrite

    Arguments:
    token -- the Eventbrite user OAuth token, used to authenticate with Eventbrite's API.

    Returns:
    resp -- the response from the API
    """
    # set headers with user token
    headers = {"Authorization": "Bearer {}".format(token)}
    # hit API and parse response
    r = requests.get("https://www.eventbriteapi.com/v3/users/me/events/", headers=headers)
    resp = r.json()
    # perform pre-processing on date and time information
    parsed_events = []
    for event in resp['events']:
        # read original date object to show it in human-friendly format
        parsed_obj = dateutil.parser.parse(event['start']['local'])
        # parse date and time into human-readable format
        parsed_date = parsed_obj.strftime('%B %d, %Y')
        parsed_time = parsed_obj.strftime('%I:%M %p')
        # parse timezone into human-readable format
        parsed_tz = event['start']['timezone'].replace("_", " ")
        # set properties in the event object for accessing in templates
        event['start_time_local'] = parsed_time
        event['start_date_local'] = parsed_date
        event['start_tz'] = parsed_tz
        # add to our events list
        parsed_events.append(event)
    # set parsed events on object and return
    resp['events'] = parsed_events
    return resp

@app.route('/')
def index():
    """Handle routing for event list page."""
    # if user is logged in, display their events, if not, redirect to login
    if "eventbrite_token" in session:
        # get user info and their events
        user_info = get_user_info(session['eventbrite_token'])
        events = get_events(session['eventbrite_token'])
        # render events
        return render_template('events_list.html', events=events['events'], user_info=user_info)
    else:
        # redirect to login page
        return redirect(url_for('login'))


@app.route('/login')
def login():
    """Handle login page routing and login logic."""
    # Eventbrite API will return a code to get the user's OAuth token
    access_code = request.args.get("code", default=None)
    # if we have it, get it and redirect, if not, show login screen
    if access_code:
        # get the app ID and client secret to hit API. This should be
        # set in the environment variables
        EVENTBRITE_SECRET = os.environ.get("EVENTBRITE_SECRET")
        EVENTBRITE_APP_KEY = os.environ.get("EVENTBRITE_APP_KEY")
        # data to hit the api requesting user token
        # look at Eventbrite docs for more info
        data = {"code": access_code,
                "client_secret": EVENTBRITE_SECRET,
                "client_id": EVENTBRITE_APP_KEY,
                "grant_type": "authorization_code"}
        # hit API and parse data
        r = requests.post("https://www.eventbrite.com/oauth/token", data=data)
        response = r.json()
        # set the access token in the user's session (user is logged in)
        session['eventbrite_token'] = response['access_token']
        # redirect to main page once logged in
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    """Log out user."""
    session.pop('eventbrite_token', None)
    return redirect(url_for('index'))
