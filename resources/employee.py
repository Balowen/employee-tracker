from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import safe_str_cmp

import uuid

from models.employee import EmployeeModel


class EmployeeRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('surname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('department',
                        type=str,
                        required=False,     # default is IT
                        help="This field cannot be left blank!")

    def post(self):
        """registers new employee if it doesn't exist already"""
        data = EmployeeRegister.parser.parse_args()
        new_employee_id = str(uuid.uuid4())

        while EmployeeModel.find_by_id(new_employee_id):
            # if this id is already in use
            new_employee_id = str(uuid.uuid4())

        employee = EmployeeModel(**data, employee_id=new_employee_id)
        employee.save_to_db()

        return {"message": "Employee successfully added to the system"}, 201  # 201 - Created


class Employee(Resource):
    """Used to check if this id_card belongs to real employee"""

    # parser = reqparse.RequestParser()   # for put request
    # parser.add_argument('employee_id',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be left blank!")

    @classmethod
    @jwt_required
    def get(cls, employee_id):
        employee = EmployeeModel.find_by_id(employee_id)
        if not employee:
            return {'message': 'Employee not found, or you do not have the access'}, 404
        else:
            """TODO:
            welcome :)
            employee.start_working_hours"""
        return employee.json()

    @jwt_required
    def put(self, employee_id):
        """Method to update employee's leaving hour"""
        # data = Employee.parser.parse_args()

        employee = EmployeeModel.find_by_id(employee_id)
        if employee is None:
            return {'message': "There is no employee with this ID, or your access_token is invalid."}
        else:
            """TODO:
            employee.update_leaving_hours()"""

        employee.save_to_db()

        return employee.json()


class EmployeeLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('employee_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    @classmethod
    def post(cls):
        # get data from parser
        data = cls.parser.parse_args()

        # find user in database
        employee = EmployeeModel.find_by_id(data['employee_id'])

        # check id/hash
        if employee and safe_str_cmp(employee.employee_id, data['employee_id']):
            access_token = create_access_token(identity=employee.employee_id)
            return {
                'access_token': access_token
            }, 200

        return {'message': 'Invalid credentials'}, 401
