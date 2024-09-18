from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask.cli import FlaskGroup
from app import app, db

cli = FlaskGroup(app)

@cli.command('db_upgrade')
def db_upgrade():
    """Run database migrations."""
    from flask_migrate import upgrade
    upgrade()

@cli.command('db_downgrade')
def db_downgrade():
    """Revert database migrations."""
    from flask_migrate import downgrade
    downgrade()

if __name__ == '__main__':
    cli()