from models.employee import EmployeeModel
from werkzeug.security import safe_str_cmp


def authenticate(unique_id):
    employee = EmployeeModel.find_by_id(unique_id)
    if employee and safe_str_cmp(employee.employee_id, unique_id):
        return employee


def identity(payload):
    # payload is the contents of the JWT token
    # this function extracts the user ID
    user_id = payload['identity']
    return EmployeeModel.find_by_id(user_id)
