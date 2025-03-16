from flask import Flask, render_template, url_for
from flask_migrate import Migrate  # type: ignore
from flask_login import LoginManager, UserMixin  # type: ignore
from wtforms import StringField, PasswordField, SubmitField  # Mengimpor hanya elemen yang dibutuhkan
from wtforms.validators import InputRequired, Length, ValidationError
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)