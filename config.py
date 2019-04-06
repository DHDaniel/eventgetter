import os

# get the secret key for Flask sessions. Must be set in environment variables.
SECRET_KEY = os.environ.get("SECRET_KEY", default=None)

if not SECRET_KEY:
    raise ValueError("No secret key set for Flask application")
