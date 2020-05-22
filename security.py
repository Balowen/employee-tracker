from models.employee import EmployeeModel
from werkzeug.security import safe_str_cmp
from flask_jwt import jwt


def authenticate(employee_id):
    employee = EmployeeModel.find_by_id(employee_id)
    if employee and safe_str_cmp(employee.employee_id.encode('utf-8'), employee_id.encode('utf-8')):
        return employee


def identity(payload):
    # payload is the contents of the JWT token
    # this function extracts the user ID
    employee_id = payload['identity']
    return EmployeeModel.find_by_id(employee_id)
