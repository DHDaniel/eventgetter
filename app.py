from flask import Flask, session, request, render_template, redirect, url_for
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
    return render_template('login.html')
