import unittest
from coverage import coverage
from flask_script import Manager
from src.api import create_app_blueprint

COV = coverage(
    branch=True,
    include='main/*',
    omit=[
        '__init__.py',
        'main/*/__init__.py'
        'main/import_policy/*'
        'main/models/*'
        'main/static/*'
        'main/templates/*',
        'settings.py',
        'tests/*',
        'wsgi.py'
    ]
)

COV.start()
app = create_app_blueprint('development')
manager = Manager(app)

@manager.command
def tests(): # Run tests
    test_suite = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def tests_with_coverage(): 
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        COV.report()
        COV.html_report(directory='tests/coverage')
        COV.erase()
        return 0
    return 1

if __name__ == '__main__':
    manager.run()