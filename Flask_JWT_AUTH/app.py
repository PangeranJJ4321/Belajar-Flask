from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required
from dotenv import load_dotenv
import os


app = Flask(__name__)
app.config.from_prefixed_env("JWT_SECRET_KEY")

jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True)