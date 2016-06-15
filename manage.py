import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db
from app.models import User, Bucketlist, Item

basedir = os.path.abspath(os.path.dirname(__file__))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    '''Returns application and database instances
    to the shell importing them automatically
    on `python manager.py shell`.
    '''
    return dict(app=app, db=db, User=User, Bucketlist=Bucketlist, Item=Item)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
