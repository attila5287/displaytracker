from flask import request
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from squares.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class ItemForm(FlaskForm):
    pass
    manufacturer = StringField(
        'Manufacturer', validators=[DataRequired()], default='Manufacturer')
    catalog_fullname = StringField(
        'Catalog Name', default='Catalog Full Name')
    color_primary = StringField(
        'Primary Color', validators=[DataRequired()], default='Primary Color')
    color_secondary = StringField(
        'Secondary Color', default='Secondary Color')
    imageclean_url = StringField(
        'ImgURL TrsPNG',  default='http://image.trnsprnt.background')
    imagewhtbg_url = StringField(
        'ImgURL WhtBg',  default='http://image.white.background')
    product_url = StringField(
        'Product', default='http://brand.product.info'
        )
    
    is_snapback = SelectField('Snapback?',
                              choices=[('no', 'NO'), ('yes', 'YES')], default='no')
    is_adjustable = SelectField('Velcro/Strap?',
                                choices=[('no', 'NO'), ('yes', 'YES')], default='no')
    is_flexfit = SelectField('Flexfit',
                             choices=[('no', 'NO'), ('yes', 'YES')], default='no')
    is_youth = SelectField('Youth',
                           choices=[('no', 'NO'), ('yes', 'YES')],  default='no')
    is_fitted = SelectField('Fitted',
                            choices=[('no', 'NO'), ('yes', 'YES')],  default='no')
    has_structcrwn = SelectField('Has structured crown?',
                                choices=[('no', 'NO'), ('yes', 'YES')], default='yes')
    has_curvedbill = SelectField('Has curved bill?',
                                 choices=[('no', 'NO'), ('yes', 'YES')], default='no')
    has_flatbill = SelectField('Has flat bill?',
                               choices=[('no', 'NO'), ('yes', 'YES')],  default='no')
    inv_lowinstock = SelectField('Low In Stocks?',
                                 choices=[('no', 'NO'), ('yes', 'YES')],  default='no')
    inv_outofstock = SelectField('Out of Stock?',
                                 choices=[('no', 'NO'), ('yes', 'YES')], default='no')

class CSVReaderForm(FlaskForm):
    csv_file = FileField(
        'Inv CSV Feed',
        validators=[
        FileAllowed(['csv'])
        ]
        )
    submit = SubmitField('Feed Inv | Read CSV')





# @app.route("/pie")
# def rick():
#     pass
#     lyrics = get_lyrics()
#     labels, values = zip(*lyrics.items())
#     data = [{
#         "labels": labels,
#         "values": values,
#         "type": "pie"}]

#     return jsonify(data)
