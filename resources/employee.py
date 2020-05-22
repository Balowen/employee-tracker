from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
import uuid

from models.employee import EmployeeModel


class Employee(Resource):
    """Used to check if this id_card belongs to real employee"""

    parser = reqparse.RequestParser()   # for put request
    parser.add_argument('employee_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    @classmethod
    @jwt_required()
    def get(cls):
        employee = EmployeeModel.find_by_id(current_identity.id)
        if not employee:
            return {'message': 'Employee not found, or you do not have the access'}, 404
        else:
            """TODO:
            welcome :)
            employee.start_working_hours"""
        return employee.json()


    @jwt_required()
    def put(self):
        """Method to update employee's leaving hour"""
        data = Employee.parser.parse_args()

        employee = EmployeeModel.find_by_id(current_identity.id)
        if employee is None:
            return {'message': "There is no employee with this ID, or your access_token is invalid."}
        else:
            """TODO:
            employee.update_leaving_hours()"""

        employee.save_to_db()

        return employee.json()
