from database import db

class User(db.Model):
    # add records here
    user = db.Column(db.Integer. primary_key=True)
    userFirstName = db.Column(db.String(50), unique=True, nullable=False)
    userLastName = db.Column(db.String(50), unique=True, nullable=False)
    userPassword = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    # add parameters for each field
    def __init__(self, user, userFirstName, userLastName, userPassword, email):
        print()
        pass

class Event(db.Model):
    # add records here
    event = db.Column(db.Integer. primary_key=True)
    hostID = db.Column(db.Integer. primary_key=True)
    eventName = db.Column(db.String(50), unique=True, nullable=False)
    eventPrivate = db.Column(db.String(50), unique=True, nullable=False)
    eventLocation = db.Column(db.String(50), unique=True, nullable=False)
    eventStartTime = db.Column(db.String(50), unique=True, nullable=False)
    eventEndTime = db.Column(db.String(50), unique=True)
    eventDescription = db.Column(db.String(50), char(1000), unique=True, nullable=False)
    # add parameters for each field
    def __init__(self):
        pass

class RSVP(db.Model):
    # same as above
    user = db.Column(db.Integer. primary_key=True)
    userName = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    pass

