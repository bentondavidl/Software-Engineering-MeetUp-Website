"""Main entry point for flask application"""

# imports
import os                 # os is used to get environment variables IP & PORT
from datetime import datetime
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template, request, redirect, url_for, session, send_file
from database.database import db
from database.models import *
import bcrypt
from forms import *
from sqlalchemy import asc, desc

app = Flask(__name__)     # create an app

# set up db location and special flags
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meetup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'BringMeTheMelons'

db.init_app(app)

# create database within the context of the app
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def index():
    """landing page for the meetup application

    Displays the homepage with all public events. 
    Both the `/` and `/index` routes call this method.
    """
    events = db.session.query(Event).filter_by(is_private=False).all()
    return render_template('index.html', events=events)

@app.route('/events', methods=['GET','POST'])
def event_list():
    """Event list page

    This page displays all of the events that are 
    either public or are owned by the current user. 
    This page is accessible via the `/events` route.

    If there is no user logged in, it redirects to the login page.
    """
    events_form = EventsForm()
    if session.get('user'):
        if request.method == 'POST':
            events = None
            if request.form.get('sort_order') == 'O':
                public_events = db.session.query(Event).filter_by(is_private=False).order_by(asc(Event.id)).all()
                host_events = db.session.query(Event).filter_by(host_id=session.get('user_id'), is_private=True).order_by(asc(Event.id)).all()
                events = public_events + host_events
            if request.form.get('sort_order') == 'N':
                public_events = db.session.query(Event).filter_by(is_private=False).order_by(desc(Event.id)).all()
                host_events = db.session.query(Event).filter_by(host_id=session.get('user_id'), is_private=True).order_by(desc(Event.id)).all()
                events = public_events + host_events
            if request.form.get('sort_order') == 'M':
                events = db.session.query(Event).filter_by(host_id=session.get('user_id')).order_by(Event.name).all()
            return render_template('events.html', events=events, form=events_form)
        else:
            public_events = db.session.query(Event).filter_by(is_private=False).all()
            host_events = db.session.query(Event).filter_by(host_id=session.get('user_id')).all()
            events = set(public_events + host_events)
            return render_template('events.html', events=events, form=events_form)
    return redirect(url_for('login'))

@app.route('/events/<int:event_id>')
def event(event_id: int):
    """Event details page

    Page for showing a specific event. On this page, users are able to 
    view all of the details of an event. If they are logged in as the host, 
    they are able to edit or delete the event. Otherwise, they are able to 
    RSVP. This is accessible via the `/events/<event_id>` route where event
    ID is the `event_id` parameter.

    If there is no user logged in, it redirects to the login page.

    Parameters
    ----------
    event_id : int
        ID of the event to be displayed on the page.
    """
    if session.get('user'):
        form = RSVPForm()
        event = db.session.query(Event).filter_by(id=event_id).one()
        host_name = db.session.query(User).filter_by(id=event.host_id).one().first_name
        is_host = event.host_id == session.get('user_id')
        return render_template('event.html', event=event, host_name=host_name,
         is_host=is_host, form=form)

    return redirect(url_for('login'))

@app.route('/events/new', methods=['GET','POST'])
def new_event():
    """Create event page

    This page hosts a form that allows users to create a new event.
    Users must provide an event name, start/end time, location, and description
    to create a valid event. They are also able to mark it as private or add an
    image. On `POST` the filled form is converted to a database entry and the
    user is redirected to the newly created event page.
    This page is accessible via the `/events/new` route

    If there is no user logged in, it redirects to the login page.
    """
    event_form = EventForm()

    if session.get('user'):
        if request.method == 'POST':
            # fix with actual field names
            name = request.form.get('name')
            host = session.get('user_id') # person who creates it is assumed the host

            # need to format start and end time
            start_time = datetime.strptime(request.form.get('start_time').strip(), '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(request.form.get('end_time').strip(), '%Y-%m-%d %H:%M')

            location = request.form.get('location')
            description = request.form.get('description')

            # optional
            is_private = True if request.form.get('is_private') == 'y' else False
            # passcode = request.form.get('passcode')

            # max_occupancy = request.form.get('max_occupancy')
            image = request.form.get('image')

            # create event object
            event = Event(name=name, host_id=host, start_time=start_time,
                    end_time=end_time, location=location,image = image, description=description,
                    is_private=is_private)

            # add to db
            db.session.add(event)
            db.session.commit()
            # get id of newly created event
            event_id = int(event.id)

            # after creation, send user to page of the new event
            return redirect(url_for('event', event_id=event_id))
        else:
            return render_template('new_event.html', form=event_form)
    return redirect(url_for('login'))

@app.route('/events/edit/<event_id>', methods=['GET','POST'])
def update_event(event_id: int):
    """Event edit page

    This page allows users to edit an existing event. On `GET`, users
    are presented with a prefilled form with current event details 
    which they are then able to edit. On `POST`, the edits in the form
    are committed to the database and users are redirected to the updated
    event's page.
    This page is accessible via the `/events/edit/<event_id>` route

    Parameters
    ----------
    event_id : int
        ID of the event to edit
    """
    event_form = EventForm()

    if request.method == 'POST':
        # event names cannot be updated after creation
        name = request.form.get('name')

        # need to format start and end time
        start_time = datetime.strptime(request.form.get('start_time').strip(), '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(request.form.get('end_time').strip(), '%Y-%m-%d %H:%M')

        location = request.form.get('location')
        description = request.form.get('description')

        # optional
        is_private = True if request.form.get('is_private') == 'y' else False
        # passcode = request.form.get('passcode')

        # max_occupancy = request.form.get('max_occupancy')
        image = request.form.get('image')

        # get existing event from db
        event = db.session.query(Event).filter_by(id=event_id).one()

        # update event properties
        event.start_time = start_time
        event.end_time = end_time
        event.location = location
        event.image = image
        event.description = description
        event.is_private = is_private

        db.session.add(event)
        db.session.commit()

        return redirect(url_for('event', event_id=event_id))
    else:
        # get event from db
        event = db.session.query(Event).filter_by(id=event_id).one()
        print(event)
        # populate fields with current values
        event_form['name'].data = event.name

        event_form['start_time'].data = event.start_time
        event_form['end_time'].data = event.end_time
        event_form['location'].data = event.location
        event_form['image'].data = event.image
        event_form['description'].data = event.description
        event_form['is_private'].data = event.is_private

        return render_template('new_event.html', event=event, form=event_form)

@app.route('/events/delete/<event_id>', methods=['POST'])
def delete(event_id):
    """Delete event

    This cannot be accessed by `GET` and only accepts `POST` 
    requests to prevent unauthorized deletion of events. When
    it is accessed, the event with the given id is removed from
    the database.

    Parameters
    ----------
    event_id : int
        ID of the event to delete
    """
    # get event from db
    if session.get('user'):
        # retrieve note from db
        event = db.session.query(Event).filter_by(id=event_id).one()
        db.session.delete(event)
        db.session.commit()

        return redirect(url_for('event_list'))
    else:
        return redirect(url_for('login'))

@app.route('/events/<event_id>/rsvp', methods=['POST'])
def rsvp(event_id):
    """RSVP to event

    This method facilitates the RSVP functionality for users
    to events. It only accepts `POST` requests so that it 
    must be called from an event's details page. When this is called,
    it takes the data from the RSVP form and creates a new 
    record in the database.

    Parameters
    ----------
    event_id : int
        ID of the event to RSVP to
    """
    if session.get('user'):
        comment_form = RSVPForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            is_going = True if request.form['is_going'] == 'y' else False
            guests = int(request.form['guests'])
            new_record = RSVP(user_id=session.get('user_id'), event_id=int(event_id), is_going=is_going, guests=guests)
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('event', event_id=event_id))

    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    """Login page

    This page allows users to log in to the application.
    On `GET`, it presents users with a login form. On 
    `POST`, it verifies that the user exists in the database and
    adds their id and name to the session. Once a user is logged in, 
    they are redirected to the public list of events.
    This page can be accessed via the `/login` route
    """
    login_form = LoginForm()

    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()

        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id

            return redirect(url_for('event_list'))

        login_form.password.errors = ['Incorrect username or password.']
        return render_template('login.html', form=login_form)

    else:
        return render_template('login.html', form=login_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user page

    This page allows users to register to the application.
    On `GET`, it presents users with a registration form` asking
    for a password, first and last name, and email address.
    On `POST`, it creates a new user with a hashed password
    and commits it to the database. Users are then redirected to
    the event list page. It also automatically logs the user in 
    by adding their first name and user id to the session.
    This page is accessible via the `/register` route
    """
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
        return redirect(url_for('event_list'))

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    """Logout function

    Clears the session entirely which effectively logs the user out of the application.
    Once this is done, the user is redirected back to the home page
    """
    if session.get('user'):
        session.clear()
    return redirect(url_for('index'))

@app.route('/events/<event_id>/download')
def download_iCal(event_id):
    """iCal export functionality

    This generates an iCal (.ics) file for the provided event and sends it
    to the browser to be downloaded. This allows for events created on this
    site to be added to external calendar applications.

    Parameters
    ----------
    event_id : int
        ID of the event to export
    """
    event = db.session.query(Event).filter_by(id=event_id).one()
    
    with open('event_export.ics', 'w') as f:
        f.write(f'''BEGIN:VCALENDAR
BEGIN:VEVENT
DESCRIPTION:{event.description}
DTEND:{event.end_time.strftime('%Y%m%dT%H%M%S')}
DTSTART:{event.start_time.strftime('%Y%m%dT%H%M%S')}
LOCATION:{event.location}
SUMMARY:{event.name}
TZID:America/New_York
END:VEVENT
END:VCALENDAR''')
    return send_file('event_export.ics', as_attachment=True)


# start application locally at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
