"""Main entry point for flask application"""

# imports
import os                 # os is used to get environment variables IP & PORT
import time
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template 

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


# start application locally at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)