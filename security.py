from models.employee import EmployeeModel
from werkzeug.security import safe_str_cmp


def authenticate(username, employee_id):
    user = EmployeeModel.find_by_username(username)
    if user and safe_str_cmp(user.password, employee_id):
        return user


def identity(payload):
    # payload is the contents of the JWT token
    # this function extracts the user ID
    user_id = payload['identity']
    return EmployeeModel.find_by_id(user_id)