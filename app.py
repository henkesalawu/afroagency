from flask import Flask, jsonify, request, abort
from models import Dancer, Event, db
from auth import requires_auth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config
import re

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

# GET /dancers - public route to get all dancers
@app.route('/dancers', methods=['GET'])
def get_dancers():
    dancers = Dancer.query.all()
    return jsonify({'success': True, 'dancers': [d.serialize() for d in dancers]}), 200

# GET /events - public route to get all events
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify({'success': True, 'events': [e.serialize() for e in events]}), 200

# GET /dancers/<id> - requires permission get:dancer-details
@app.route('/dancers/<int:id>', methods=['GET'])
@requires_auth('get:dancer-details')
def get_dancer_details(id):
    dancer = Dancer.query.get(id)
    if not dancer:
        abort(404)
    return jsonify({'success': True, 'dancer': dancer.serialize()}), 200

# GET /events/<id> - requires permission get:event-details
@app.route('/events/<int:id>', methods=['GET'])
@requires_auth('get:event-details')
def get_event_details(id):
    event = Event.query.get(id)
    if not event:
        abort(404)
    return jsonify({'success': True, 'event': event.serialize()}), 200

# POST /dancers - requires permission add:dancer
@app.route('/dancers', methods=['POST'])
@requires_auth('add:dancer')
def add_dancer():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    phone = data.get('phone')
    website = data.get('website')

    if not name or not age or not gender:
        abort(400)

    new_dancer = Dancer(name=name, age=age, gender=gender, phone=phone, website=website)
    new_dancer.insert()

    return jsonify({'success': True, 'dancer': new_dancer.serialize()}), 201

# POST /events - requires permission add:event
@app.route('/events', methods=['POST'])
@requires_auth('add:event')
def add_event():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    date = data.get('date')

    if not name or not address or not date:
        abort(400)

    new_event = Event(name=name, address=address, date=date)
    new_event.insert()

    return jsonify({'success': True, 'event': new_event.serialize()}), 201

# PATCH /dancers/<id> - requires permission edit:dancer
@app.route('/dancers/<int:id>', methods=['PATCH'])
@requires_auth('edit:dancer')
def update_dancer(id):
    dancer = Dancer.query.get(id)
    if not dancer:
        abort(404)

    data = request.get_json()

    dancer.name = data.get('name', dancer.name)
    dancer.age = data.get('age', dancer.age)
    dancer.gender = data.get('gender', dancer.gender)
    dancer.phone = data.get('phone', dancer.phone)
    dancer.website = data.get('website', dancer.website)

    dancer.update()

    return jsonify({'success': True, 'dancer': dancer.serialize()}), 200

# PATCH /events/<id> - requires permission edit:event
@app.route('/events/<int:id>', methods=['PATCH'])
@requires_auth('edit:event')
def update_event(id):
    event = Event.query.get(id)
    if not event:
        abort(404)

    data = request.get_json()

    event.name = data.get('name', event.name)
    event.address = data.get('address', event.address)
    event.date = data.get('date', event.date)

    event.update()

    return jsonify({'success': True, 'event': event.serialize()}), 200

# DELETE /dancers/<id> - requires permission delete:dancer
@app.route('/dancers/<int:id>', methods=['DELETE'])
@requires_auth('delete:dancer')
def delete_dancer(id):
    dancer = Dancer.query.get(id)
    if not dancer:
        abort(404)

    dancer.delete()

    return jsonify({'success': True, 'deleted': id}), 200

# DELETE /events/<id> - requires permission delete:event
@app.route('/events/<int:id>', methods=['DELETE'])
@requires_auth('delete:event')
def delete_event(id):
    event = Event.query.get(id)
    if not event:
        abort(404)

    event.delete()

    return jsonify({'success': True, 'deleted': id}), 200

# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"success": False, "error": 403, "message": "forbidden"}), 403

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"success": False, "error": 401, "message": "unauthorized"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
