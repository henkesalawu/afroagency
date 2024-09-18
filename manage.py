import os
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import db, Dancer, Event  # Import your models here

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/yourlocaldb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['AUTH0_DOMAIN'] = os.environ.get('AUTH0_DOMAIN')
    app.config['API_IDENTIFIER'] = os.environ.get('API_IDENTIFIER')
    app.config['AUTH0_CLIENT_ID'] = os.environ.get('AUTH0_CLIENT_ID')
    app.config['AUTH0_CLIENT_SECRET'] = os.environ.get('AUTH0_CLIENT_SECRET')

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from app import app as application
        return app

app = create_app()

# Initialize Flask-Script Manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def runserver():
    """Run the Flask development server."""
    app.run(debug=True)

if __name__ == '__main__':
    manager.run()