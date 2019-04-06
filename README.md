# Eventgetter

## Setting up

All you need to run this app is to set the appropriate environment variables. The ones required are:

- `SECRET_KEY`: a random hash that will be used by Flask to encrypt user sessions.
- `APP_SETTINGS`: must be set to `config.py`.
- `EVENTBRITE_APP_KEY`: the Eventbrite app ID retrieved from your Eventbrite account. It is the key that identifies your application with Eventbrite.
- `EVENTBRITE_SECRET`: the secret key of your Eventbrite app, retrieved from your Eventbrite account. It is used to interact with the Eventbrite API along with the app key.


## Running locally
The best way to run locally is to use the Flask `run` command. For this, you must set an additional environment variable, `FLASK_APP=app.py`. After this, simply run `flask run` in the terminal.

**Note**: the Eventbrite API will not recognize the `localhost:5000` URL, so login will not work if you run the project locally. A quick fix is to do the following:

1. In the application details of your Eventbrite app, retrieve the Application URL and the OAuth Redirect URI.
2. Paste the following command on your browser: `https://www.eventbrite.com/oauth/authorize?response_type=token&client_id=BRD34KZ3IVG7CPYL7K&redirect_uri=your_application_URL`
3. You should then be redirected by Eventbrite to the application URL you set with a hash appended at the end, which will contain the `access_token`. Copy and paste this value.
4. In the file `app.py`, inside the `index()` function, insert the following line of code before anything else: `session['eventbrite_token'] = your_copy_pasted_token`
5. Run the app locally using `flask run`

**Important**: delete this line of code if you are deploying to the real URL. This is just for testing the app locally and making sure the mechanics of it all work.
