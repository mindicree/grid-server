from flask import Blueprint

generic_routes = Blueprint('generic_routes', __name__)

@generic_routes.route('/testing_testing')
def testing_testing():
    return 'TESTING! DO YOU READ?!'

@generic_routes.route('/')
def index():
    return "Hello, GRID!"