from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date

db = SQLAlchemy()

# Set up the database connection
def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

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
