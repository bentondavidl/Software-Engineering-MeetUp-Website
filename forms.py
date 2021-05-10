from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, IntegerField, RadioField
from wtforms.fields.core import BooleanField
from wtforms.validators import Length, DataRequired, EqualTo, Email
from wtforms import ValidationError
from database.models import User
from database.database import db


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    firstname = StringField('First Name', validators=[Length(1, 10)])

    lastname = StringField('Last Name', validators=[Length(1, 10)])

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=10)
    ])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Username already in use.')

class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")
    ])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')

class EventForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField('Event Title', [DataRequired(message='The event must have a name')])

    start_time = DateTimeField('Start Time', Format: YYYY-MM-DD HH:MM', [DataRequired(message='When is your event?')])
    end_time = DateTimeField('End Time', [DataRequired(message='When is your event?')])

    location = StringField('Location', [DataRequired(message='Where is your event?')])

    description = TextAreaField('Event Description', validators=[Length(min=1)])

    is_private = BooleanField('Private Event?')

    image = StringField('Image')

    submit = SubmitField('Create Event')

    def validate_on_submit(self):
        result = super(EventForm, self).validate()
        if self.start_time.data > self.end_time.data:
            return False
        return result


class RSVPForm(FlaskForm):
    class Meta:
        csrf = False

    is_going = BooleanField('Are you going?')
    guests = IntegerField('How many guests, including you, are attending?')

    submit = SubmitField('Send RSVP')

class EventsForm(FlaskForm):
    class Meta:
        csrf = False



    sort_order = RadioField('sort_order', choices=[('O','Oldest Event First'),('N','Newest Event First'),('M','My Events')])


    submit = SubmitField('Sort')
