from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# class Visitor(db.Model):
#     visitor_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     email = db.Column(db.String(255))
#     phone_number = db.Column(db.String(20))

class Guards(db.Model, UserMixin):
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)

# class Visit(db.Model):
#     visit_id = db.Column(db.Integer, primary_key=True)
#     tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.tenant_id'))
#     visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.visitor_id'))
#     guard_id = db.Column(db.Integer, db.ForeignKey('guard.guard_id'))
#     check_in_time = db.Column(db.TIMESTAMP)
#     check_out_time = db.Column(db.TIMESTAMP)

#     tenant = db.relationship('Tenant', backref='visits')
#     visitor = db.relationship('Visitor', backref='visits')
#     guard = db.relationship('Guard', backref='visits')
class Visits(db.Model):
    visit_id = db.Column(db.Integer, primary_key=True)
    visitor_first_name = db.Column(db.String(50), nullable=False)
    visitor_last_name = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50))
    phone = db.Column(db.String(20), nullable=False)
    visitor_destination = db.Column(db.String(100), nullable=False)
    visit_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"Visit(visitor_first_name='{self.visitor_first_name}', visitor_last_name='{self.visitor_last_name}', visit_time='{self.visit_time}')"

class Tenants(db.Model, UserMixin):
    tenant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    estate = db.Column(db.String(50), nullable=False)
    block = db.Column(db.String(20), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    def get_id(self):
        return str(self.tenant_id)

    def __repr__(self):
        return f'<User {self.username}>'

