from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, ValidationError,TextField
from wtforms.validators import DataRequired,EqualTo,Email,Length, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "eg. joe@example.com"})
    password = PasswordField('Password', validators=[InputRequired()])

class SignupForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "eg. joe@example.com"})
    gender = SelectField('Gender', choices=[('Male','Male'), ('Female', 'Female')])
    date_of_birth = StringField('D.O.B', validators=[DataRequired()])
    street = TextField('Street', validators=[DataRequired()])
    city = TextField('City', validators=[DataRequired()])
    parish = TextField('Parish', validators=[DataRequired()])
    telephone = StringField('Telephone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=5,max=100,message="must be aleast 6 characters or more"),EqualTo('confirmpassword', message='Passwords must match')])
    confirmpassword = PasswordField('ConfirmPassword', validators=[DataRequired()])
    
class UploadForm(FlaskForm):
    photo = FileField('Photo',validators=[FileRequired(),FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',"file allowed"])])
    description = StringField('Description', validators=[DataRequired()])
    # detail=TextAreaField('detail', validators=[DataRequired()])

class Creditcard(FlaskForm):
    cardNum =StringField('Card Number', validators=[DataRequired()])
    name_on_card =StringField('Name_on_card', validators=[DataRequired()])
    card_security_code =StringField('Card_security_code', validators=[DataRequired(),Length(min=3,max=3,message="must be 3 numbers")])
    expiration_month =StringField('Expiration_month', validators=[DataRequired()])
    expiration_year =StringField('Expiration_year', validators=[DataRequired()])
    billing_street =StringField('Billing_street', validators=[DataRequired()])
    billing_city =StringField('Billing_city', validators=[DataRequired()])
    billing_parish =StringField('Billing_parish', validators=[DataRequired()])
    
class Search(FlaskForm):
    search =StringField('search', validators=[DataRequired()])