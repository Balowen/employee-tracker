import os

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # turns off flask_sqlalchemy modification tracker
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'bart'


api = Api(app)