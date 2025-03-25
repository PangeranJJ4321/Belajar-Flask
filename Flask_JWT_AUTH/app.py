from flask import Flask
from extensions import db, jwt
from dotenv import load_dotenv
from auth import auth_blueprint
from users import user_bluprint

# Load .env
load_dotenv()

app = Flask(__name__)

# Load konfigurasi dari environment variables dengan prefix FLASK_
app.config.from_prefixed_env()


db.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(user_bluprint, url_prefix="/users")

if __name__ == "__main__":
    app.run(debug=True)
