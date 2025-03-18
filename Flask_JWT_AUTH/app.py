from flask import Flask
from extensions import db
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)

# Load konfigurasi dari environment variables dengan prefix FLASK_
app.config.from_prefixed_env()


db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
