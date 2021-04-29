"""Definition of database tables"""

from database.database import db

class User(db.Model):
    # add records here
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(50), nullable=False)
    last_name = db.Column('last_name', db.String(50), nullable=False)
    password = db.Column('password', db.String(50), nullable=False)
    email = db.Column('email', db.String(50), unique=True, nullable=False)
    events = db.relationship('Event', backref='user', lazy=True)
    rsvps = db.relationship('RSVP', backref='user', lazy=True)
    # add parameters for each field
    def __init__(self, first_name, last_name, password, email):
        """Create User instance

        Parameters
        ----------
        first_name : str
            User's first name
        last_name : str
            User's last name
        password : str
            User's hashed password
        email : str
            Email address of the user
        """
        self.first_name = first_name
        self.last_name = last_name 
        self.password = password
        self.email = email

class Event(db.Model):
    # add records here
    id = db.Column('id', db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column('name', db.String(100), nullable=False)
    is_private = db.Column('is_private', db.Boolean, default=False, nullable=False)
    location = db.Column('location', db.String(200), nullable=False)
    start_time = db.Column('start_time', db.DateTime, nullable=False)
    end_time = db.Column('end_time', db.DateTime)
    description = db.Column('description', db.VARCHAR, nullable=False)
    rsvps = db.relationship('RSVP', backref='event', cascade='all, delete-orphan', lazy=True)
    # add parameters for each field
    def __init__(self, host_id, name, is_private, location, start_time, end_time, description):
        """Create Event record

        Parameters
        ----------
        host_id : int
            User ID of the event host/creator
        name : str
            Name of the event
        is_private : bool
            True if private, False if public
        location : str
            Where the event is to be held
        start_time : datetime
            Day and time for event to start
        end_time : datetime
            Day and time for event to end
        description : str
            Description of the event
        """
        self.host_id = host_id
        self.name = name
        self.is_private = is_private
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.description = description


class RSVP(db.Model):
    # same as above
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    is_going = db.Column('is_going',db.Boolean, default=False, nullable=False)
    guests = db.Column('guests', db.SmallInteger, nullable=False)

    def __init__(self, user_id, event_id, is_going, guests=0):
        """Create RSVP instance

        Parameters
        ----------
        user_id : int
            User that is responding to the event
        event_id : int
            ID of the event being responded to
        is_going : bool
            True if they are going, False if they are not
        guests : int, optional
            number of guests, not including respondant, attending the event, by default 0
        """
        self.user_id = user_id
        self.event_id = event_id
        self.is_going = is_going
        self.guests = guests
    


