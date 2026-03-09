from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateField, TimeField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    employee_id = StringField('Employee ID', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    employee_id = StringField('Employee ID', validators=[DataRequired(), Length(min=3, max=50)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    department = SelectField('Department', choices=[
        ('production', 'Production Department'),
        ('hr', 'Human Resources'),
        ('it', 'IT Department'),
        ('quality', 'Quality Management')
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_employee_id(self, field):
        if User.query.filter_by(employee_id=field.data).first():
            raise ValidationError('Employee ID already exists')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

class OvertimeForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    reason = TextAreaField('Reason', validators=[DataRequired(), Length(min=10, max=500)])

class MealRegistrationForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    has_meal = BooleanField('Register for meal')
    notes = TextAreaField('Notes', validators=[Length(max=200)])

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
