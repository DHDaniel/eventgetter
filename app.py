from flask import Flask, session, request, render_template
app = Flask(__name__)

app.config.from_envvar("APP_SETTINGS")

@app.route('/')
def index():
    session["works"] = True
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return session["works"]
    else:
        return "This is the login page"
