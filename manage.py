import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
