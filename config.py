import os

SECRET_KEY = os.environ.get("SECRET_KEY", default=None)

if not SECRET_KEY:
    raise ValueError("No secret key set for Flask application")
