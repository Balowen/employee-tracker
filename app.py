import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.employee import Employee, EmployeeRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # turns off flask_sqlalchemy modification tracker
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'tracker'


api = Api(app)


# @app.before_first_request
# def create_tables():
#     db.create_all()


jwt = JWT(app, authenticate, identity)  # creates /auth endpoint
api.add_resource(EmployeeRegister, '/register')
api.add_resource(Employee, '/employee/<string:employee_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)