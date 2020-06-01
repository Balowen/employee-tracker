from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import safe_str_cmp
from datetime import datetime
import uuid

from models.employee import EmployeeModel
from models.workday import WorkdayModel


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
        """registers new employee if it doesn't exist already,
            this endpoint simulates assigning a new ID card to an employee,
            clearly it should be more safe, but it's just a proof-of-concept"""
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

    @classmethod
    @jwt_required
    def get(cls, employee_id):
        """ endpoint for testing only"""
        employee = EmployeeModel.find_by_id(employee_id)
        if not employee:
            return {'message': 'Employee not found, or you do not have the access'}, 404

        return employee.json()

    # @jwt_required
    def put(self, employee_id):
        """Method to update employee's leaving hour"""

        employee = EmployeeModel.find_by_id(employee_id)
        if employee is None:
            return {'message': "There is no employee with this ID, or your access_token is invalid."}, 404
        else:
            """ check if employee entered the building today"""
            if WorkdayModel.find_latest_workday(employee.id):
                """checking if employee already entered building today"""
                last_workday = WorkdayModel.find_latest_workday(employee.id)

                if last_workday.time_in.day == datetime.today().day:
                    last_workday.time_out = datetime.today()
                    # calculate hours_worked|   .time converts to H:M
                    duration = last_workday.time_out - last_workday.time_in
                    # duration is a datetime.timedelta
                    duration = (datetime.min + duration).time()
                    last_workday.hours_worked = duration
                    try:
                        last_workday.save_to_db()
                    except:
                        return {'message': 'An error occurred updating worked hours'}, 500

                    return last_workday.json()

        return {'message': 'First use of card, or employee did not start work today'}, 200


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
            if WorkdayModel.find_latest_workday(employee.id):
                """checking if employee already entered building today"""
                last_workday = WorkdayModel.find_latest_workday(employee.id)

                if last_workday.time_in.day == datetime.today().day:
                    """ if he entered today, only the token is returned and the workday continues"""
                    return {
                               'access_token': access_token
                           }, 200
                else:
                    workday = WorkdayModel(employee.name, employee.id)
                    try:
                        workday.save_to_db()
                    except:
                        return {'message': "An error occured creating the workingday."}, 500

                    return {
                        'access_token': access_token
                    }

            else:
                """First entrance, start a workday"""
                workday = WorkdayModel(employee.name, employee.id)
                try:
                    workday.save_to_db()
                except:
                    return {'message': "An error occured creating the workingday."}, 500

                return {
                    'access_token': access_token
                }
        return {'message': 'Invalid credentials'}, 401
