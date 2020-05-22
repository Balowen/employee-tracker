from db import db
import uuid


class EmployeeModel(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(30), default="IT", nullable=False)
    employee_id = db.Column(db.String(32), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    def __init__(self, name, surname, department, employee_id):
        self.name = name
        self.surname = surname
        self.department = department
        self.employee_id = employee_id

    def json(self):
        return{
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'department': self.department,
            'employee_id': self.employee_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(employee_id=_id).first()


