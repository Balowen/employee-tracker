import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.employee import Employee, EmployeeRegister, EmployeeLogin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # turns off flask_sqlalchemy modification tracker
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'tracker'  # or this app.config['JWT_SECRET_KEY']


api = Api(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()


jwt = JWTManager(app)
api.add_resource(EmployeeRegister, '/register')
api.add_resource(EmployeeLogin, '/login')
api.add_resource(Employee, '/employee/<string:employee_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)