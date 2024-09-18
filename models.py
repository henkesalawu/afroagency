from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

class Dancer(db.Model):
    __tablename__ = 'dancers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone = Column(String)
    website = Column(String)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'website': self.website
        }

class Event(db.Model):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'date': self.date
        }