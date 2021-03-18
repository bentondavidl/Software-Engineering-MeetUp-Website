"""Main entry point for flask application"""

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template 

app = Flask(__name__)     # create an app

# create default endpoint for application
@app.route('/')
def index():
    return render_template('index.html')

# start application locally at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)