"""Main entry point for flask application"""

# imports
import os                 # os is used to get environment variables IP & PORT
import time
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template, request, redirect, url_for, session
from database.database import db
from database.models import *
import bcrypt
from forms import *

app = Flask(__name__)     # create an app

app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///meetup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'BringMeTheMelons'

db.init_app(app)

with app.app_context():
    db.create_all()

# create default endpoint for application
@app.route('/')
def index():
    session['user'] = 'david'
    session['user_id'] = 0
    events = db.session.query(Event).filter_by(is_private=False).all()
    return render_template('index.html', events=events)

@app.route('/events')
def event_list():
    if session.get('user'):
        events = db.session.query(Event).all()
        return render_template('events.html', events=events)
    
    return redirect(url_for('login'))

@app.route('/events/<int:event_id>')
def event(event_id):
    if session.get('user'):
        events = db.session.query(Event).filter_by(event_id=event_id).one()
        return render_template('event.html', events)
    
    return redirect(url_for('login'))

@app.route('/events/new', methods=['GET','POST'])
def new_event():
    event_form = EventForm()

    if session.get('user'):
        if request.method == 'POST':
            # fix with actual field names
            name = request.form.get('name')
            host = session.get('user_id') # person who creates it is assumed the host

            # need to format start and end time
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')

            location = request.form.get('location')
            description = request.form.get('description')

            # optional
            is_private = request.form.get('is_private')
            # passcode = request.form.get('passcode')

            # max_occupancy = request.form.get('max_occupancy')
            # image = request.form.get('image_url')

            # create event object
            event = Event(name=name, host_id=host, start_time=start_time, 
                    end_time=end_time, location=location, description=description, 
                    is_private=is_private)

            # get id of newly created event
            event_id = event.id
            # add to db
            db.session.add(event)
            db.session.commit()

            # after creation, send user to page of the new event
            return redirect(url_for('event', event_id=event_id))
        else:
            return render_template('new_event.html', form=event_form)
    return redirect(url_for('login'))

@app.route('/events/edit/<event_id>', methods=['GET','POST'])
def update_event(event_id):
    event_form = EventForm()

    if request.method == 'POST':
        name = request.form.get('name')

        # need to format start and end time
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')

        location = request.form.get('location')
        description = request.form.get('description')

        # optional
        is_private = request.form.get('is_private')
        # passcode = request.form.get('passcode')

        # max_occupancy = request.form.get('max_occupancy')
        # image = request.form.get('image_url')

        # get existing event from db
        event = db.session.query(Event).filter_by(id=event_id).one()

        # update event properties
        event.start_time = start_time
        event.end_time = end_time
        event.location = location
        event.description = description
        event.is_private = is_private

        db.session.add(event)
        db.session.commit()

        return redirect(url_for('event', event_id=event_id))
    else:
        # get event from db
        event = db.session.query(Event).filter_by(id=event_id).one()

        return render_template('new_event.html', event=event, form=event_form)

@app.route('/events/delete/<event_id>', methods=['POST'])
def delete(event_id):
    # get event from db
    event = db.session.query(Event).filter_by(id=event_id).one()
    db.session.delete(event)
    db.session.commit()

    return redirect(url_for('event_list'))

@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        session['user'] = 'david'
        session['user_id'] = 0
        return redirect(url_for('get_notes'))
    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()

        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id

            return redirect(url_for('get_notes'))

        login_form.password.errors = ['Incorrect username or password.']
        return render_template('login.html', form=login_form)

    else:
        return render_template('login.html', form=login_form)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name=first_name, last_name=last_name, email=request.form['email'], password=h_password)
        # add user to db
        db.session.add(new_user)
        db.session.commit()
        # save teh user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id # access id value from user model of this new user
        # show user dashboard
        return redirect(url_for('get_notes'))

    return render_template('register.html', form=form)

# start application locally at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
