"""Main entry point for flask application"""

# imports
import os                 # os is used to get environment variables IP & PORT
import time
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template, request, redirect, url_for

app = Flask(__name__)     # create an app

# create default endpoint for application
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def event_list():
    events = {
        1: {'name':'Event 1', 'time':'4:00pm-5:00pm Feb 1', 'host':'Host 1', 'location':'Location 1', 'description':'Description 1'},
        2: {'name':'Event 2', 'time':'4:00pm-5:00pm Feb 2', 'host':'Host 2', 'location':'Location 2', 'description':'Description 2'},
        3: {'name':'Event 3', 'time':'4:00pm-5:00pm Feb 3', 'host':'Host 3', 'location':'Location 3', 'description':'Description 3'},
        4: {'name':'Event 4', 'time':'4:00pm-5:00pm Feb 4', 'host':'Host 4', 'location':'Location 4', 'description':'Description 4'},
        }
    return render_template('events.html', events)

@app.route('/events/<int:event_id>')
def event(event_id):
    events = {
        1: {'name':'Event 1', 'time':'4:00pm-5:00pm Feb 1', 'host':'Host 1', 'location':'Location 1', 'description':'Description 1'},
        2: {'name':'Event 2', 'time':'4:00pm-5:00pm Feb 2', 'host':'Host 2', 'location':'Location 2', 'description':'Description 2'},
        3: {'name':'Event 3', 'time':'4:00pm-5:00pm Feb 3', 'host':'Host 3', 'location':'Location 3', 'description':'Description 3'},
        4: {'name':'Event 4', 'time':'4:00pm-5:00pm Feb 4', 'host':'Host 4', 'location':'Location 4', 'description':'Description 4'},
        }
    return render_template('events.html', events[event_id])

@app.route('/events/new', methods=['GET','POST'])
def new_event(user_id):
    if request.method == 'POST':
        # fix with actual field names
        name = request.form.get('name')
        host = user_id # person who creates it is assumed the host

        # need to format start and end time
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')

        location = request.form.get('location')
        description = request.form.get('description')

        # optional
        is_private = request.form.get('is_private')
        passcode = request.form.get('passcode')

        max_occupancy = request.form.get('max_occupancy')
        image = request.form.get('image_url')

        # create event object

        # get id of newly created event
        event_id = 0
        # add to db

        # after creation, send user to page of the new event
        return redirect(url_for('event', event_id=event_id))
    else:
        return render_template('new_event.html')

@app.route('/events/edit/<event_id>', methods=['GET','POST'])
def update_event(event_id):
    if request.method == 'POST':
        name = request.form.get('name')

        # need to format start and end time
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')

        location = request.form.get('location')
        description = request.form.get('description')

        # optional
        is_private = request.form.get('is_private')
        passcode = request.form.get('passcode')

        max_occupancy = request.form.get('max_occupancy')
        image = request.form.get('image_url')

        # get existing event from db
        # event = db.session.query(Event).filter_by(id=event_id).first()

        # update event properties

        return redirect(url_for('event', event_id=event_id))
    else:
        # get event from db
        # event = db.session.query(Event).filter_by(id=event_id)
        event = None

        return render_template('new_event.html', event=event)


# start application locally at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)