from flask import Flask, flash, redirect, render_template, url_for
from flask_migrate import Migrate  
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
from models import db, User, UserMixin, login_maneger
from config import Config
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
login_maneger.init_app(app)
login_maneger.login_view = "login"
migrate = Migrate(app, db)

@login_maneger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placholder': 'Username'})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placholder': 'Password'})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_name = User.query.filter_by(username=username.data).first()

        if existing_user_name:
            raise ValidationError(
                "That username already axists. Please choose a different one."
            )
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placholder': 'Username'})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placholder': 'Password'})

    submit = SubmitField("Login")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login berhasil!", "seccess")
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    return "hai"

if __name__ == '__main__':
    app.run(debug=True)