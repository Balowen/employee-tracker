import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.employee import EmployeeModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # turns off flask_sqlalchemy modification tracker
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'bart'


api = Api(app)


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)