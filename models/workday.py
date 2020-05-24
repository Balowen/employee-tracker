from db import db
from datetime import datetime


class WorkdayModel(db.Model):
    __tablename__ = 'workdays'

    id = db.Column(db.Integer, primary_key=True)
    time_in = db.Column(db.DateTime(timezone=False), default=datetime.today)
    time_out = db.Column(db.DateTime(timezone=False))
    hours_worked = db.Column(db.Time, default=None)     # assign datetime.time() to it?
    worker_name = db.Column(db.String(80))

    worker_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    worker = db.relationship('EmployeeModel')

    def __init__(self, worker_name, worker_id):
        self.worker_name = worker_name
        self.worker_id = worker_id

    def json(self):
        return {'id': self.id,
                'worker_name': self.worker_name,
                "worker_id": self.worker_id,
                'time_in':  self.time_in,
                'time_out': self.time_out,
                'hours_worker': self.hours_worked
        }

    # todo
    # POST: save the start date(time_in) and assign employees credentials
    # PUT: update time_out (leaving hours), update hours_worked

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_latest_workday(cls, _id):
        return cls.query.filter_by(worker_id=_id).order_by(cls.time_in.desc()).first()

    @classmethod
    def find_employee_workdays(cls, _id):
        return cls.query.filter_by(worker_id=_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()