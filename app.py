from flask import Flask, jsonify, request, abort
from models import Dancer, Event, db
from auth import requires_auth, AuthError
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config
import re
from datetime import datetime

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

def format_date(date_string):
    return datetime.strptime(date_string, '%d-%m-%Y').strftime('%Y-%m-%d')


@app.route('/')
def home():
    return ('Welcome to Afrobeats Dance Agency')

# Display all dancers
@app.route('/dancers', methods=['GET'])
def get_dancers():
    try:
        dancers = Dancer.query.all()
    
        if len(dancers) == 0:
            abort(404)
    
        return jsonify({
            'success': True, 
            'dancers': [d.serialize() for d in dancers],
            'total_dancers':len(dancers)
        }), 200
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        abort(422)

# GET Display all events
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify({'success': True, 'events': [e.serialize() for e in events]}), 200

# Display dancer b
@app.route('/dancers/<int:id>', methods=['GET'])
@requires_auth('get:dancer-details')
def get_dancer_details(payload, id):
    dancer = Dancer.query.get(id)
    if not dancer:
        abort(404)
    return jsonify({
        'success': True, 
        'dancer': dancer.serialize()
    }), 200

# Display event
@app.route('/events/<int:id>', methods=['GET'])
@requires_auth('get:event-details')
def get_event_details(payload, id):
    event = Event.query.get(id)
    if not event:
        abort(404)
    return jsonify({'success': True, 'event': event.serialize()}), 200

# Add dancer
@app.route('/dancers', methods=['POST'])
@requires_auth('add:dancer')
def add_dancer(payload):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    phone = data.get('phone')
    website = data.get('website')

    if not name or not age or not gender:
        abort(400)
    try:
        new_dancer = Dancer(
            name=name, 
            age=age, 
            gender=gender, 
            phone=phone, 
            website=website
        )
        
        db.session.add(new_dancer)
        db.session.commit()

        return jsonify({
            'success': True, 
            'new_dancer': new_dancer.serialize()
        }), 201
    except Exception:
        abort(422)

# Add Events
@app.route('/events', methods=['POST'])
@requires_auth('add:event')
def add_event(payload):
    data = request.get_json()
    name = data['name']
    address = data['address']
    date = format_date(data['date'])

    if not name or not address or not date:
        abort(400)
    try:

        new_event = Event(
            name=name, 
            address=address, 
            date=date
        )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({
            'success': True, 
            'event': new_event.serialize()
        }), 201
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        abort(422)

# Edit dancer
@app.route('/dancers/<int:id>', methods=['PATCH'])
@requires_auth('edit:dancer')
def update_dancer(payload,id):
    dancer = Dancer.query.get(id)
    if not dancer:
        return jsonify({
            'success': False,
            'message': 'Dancer to edit not found'
        }), 404

    data = request.get_json()
    try:
        if 'name' in data:
            dancer.name = data['name']
        if 'age' in data:
            dancer.age = data['age']
        if 'gender' in data:
            dancer.gender = data['gender']
        if 'phone' in data:
            dancer.phone = data['phone']
        if 'website' in data:
            dancer.website = data['website']

        db.session.commit()

        return jsonify({
            'success': True, 
            'updated_dancer': dancer.serialize()
        }), 200
    except Exception as e:
        app.logger.error(f"Dancer could not be updated: {e}")
        db.session.rollback()
        abort(422)

# Edit event
@app.route('/events/<int:id>', methods=['PATCH'])
@requires_auth('edit:event')
def update_event(payload, id):
    event = Event.query.get(id)
    if not event:
        abort(404)

    data = request.get_json()
    try:
        if 'name' in data:
            event.name = data['name']
        if 'address' in data:
            event.address = data['address']
        if 'date' in data:
            event.date = format_date(data['date'])

        db.session.commit()

        return jsonify({
            'success': True, 
            'event': event.serialize()
        }), 200
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        abort(422)

# DELETE dancer
@app.route('/dancers/<int:id>', methods=['DELETE'])
@requires_auth('delete:dancer')
def delete_dancer(payload, id):
    
    dancer = Dancer.query.get(id)
    
    if not dancer:
        abort(404)
    try:
        db.session.delete(dancer)
        db.session.commit()

        return jsonify({
            'success': True, 
            'deleted_dancer': id
        }), 200
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        abort(422)

# DELETE event
@app.route('/events/<int:id>', methods=['DELETE'])
@requires_auth('delete:event')
def delete_event(payload, id):
    event = Event.query.get(id)

    if not event:
        abort(404)
    try:
        db.session.delete(event)
        db.session.commit()

        return jsonify({
            'success': True, 
            'deleted_event': id
        }), 200
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        abort(422)

# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400, 
        "message": "Bad request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404, 
        "message": "Resource not found/empty"
    }), 404

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False, 
        "error": 403, 
        "message": "Forbidden"
    }), 403

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False, 
        "error": 401, 
        "message": 
        "Unauthorized"
    }), 401

@app.errorhandler(422)
def unproccessable(error):
    return jsonify({
        "success": False, 
        "error": 422, 
        "message": 
        "Unable to process"
    }), 401

@app.errorhandler(AuthError)
def auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error
        }), e.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
