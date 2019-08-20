import os
import unittest
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from abovo.main import create_app, db, sio
from abovo.main.models import *


app = create_app(os.getenv('ABOVO_ENV') or 'dev')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    # run server with socket io
    sio.run(app)


@manager.command
def test():
    # run all server tests
    tests = unittest.TestLoader().discover('abovo/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
