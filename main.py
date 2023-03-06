from flask import Flask, render_template, redirect, url_for, request, send_file
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo, ValidationError
from models import db, User
from IPChecker import iptester


app = Flask(__name__)
app.config['SECRET_KEY'] = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

Bootstrap(app)

#form class
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(), 
        Length(min=2, max=15)
        ])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    # submit = SubmitField('Login', render_kw={'class':'btn btn-primary btn-lg mb-4'})

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(), 
        Length(min=2, max=15),
        
    ])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match'), Length(min=8, max=80)])
    confirm = PasswordField('Repeat Password')
    # submit = SubmitField('Register', render_kw={'class':'btn btn-primary btn-lg mb-4'})

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    form = LoginForm()
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # if validate_username(username) != "Username taken":
        print(validate_username(username))
        user = User()
        user.username = username
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return 'User registered successfully!'
        # else:
        #     return 'Username is already taken, try something else.'

    return render_template('register.html', title='Register', form=form)

@app.route('/ipscanner', methods=["GET", "POST"])
def ipscanner():
    ext = iptester()
    if request.method == 'POST':
        inp = request.form['scanner']
        ext.runthis(inp)
        return send_file("out.txt")
        # return ext.runthis(inp)
    return render_template('ipscanner.html', title="Ip scanner")

def validate_username(username):
    if User.query.filter_by(username=username).first():
        return 'Username Taken'

if __name__ == '__main__':
    app.run(debug=True)