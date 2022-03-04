from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app import db


# TODO: define DB tables
# See https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application


class Centers(db.Model):
    __tablename__ = 'Centers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    reservations = relationship('Reservation')
    lat = db.Column(db.Float,nullable=False)
    lon = db.Column(db.Float,nullable=False)

    def __repr__(self):
        return f"id: {self.id}, nazev: {self.name}"

class Reservation(db.Model):
    __tablename__ = 'Reservation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date,nullable=False)


    center_id = db.Column(db.Integer, ForeignKey("Centers.id"))
    center = relationship('Centers')
    center_name = association_proxy('center','name')



