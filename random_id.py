from random import randint
from db import db


def random_id():
    """Generates random employee id which simulates id card"""
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)

    from flask_sqlalchemy import orm

    db_session_maker = orm.sessionmaker(bind=db.engine)
    db_session = db_session_maker()
    while db_session.query(db.Employees).filter(employee_id == rand).limit(1).first() is not None:
        rand = randint(min_, max_)

    return rand