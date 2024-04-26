import os
import json
from flask import Flask, jsonify, request, session
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_mail import Mail, Message
from src.api.endpoints import get_root
from src.services.flask_setup_service.flask_setup_service import FlaskSetupService

if __name__ == '__main__':
    flask_setup = Flask(__name__, instance_relative_config=True)
    app = FlaskSetupService(flask_setup, test_config=None, config_type=None, package_name=None, package_path=None)
    app.add_endpoint('/', 'root', get_root, methods=['GET'])
    app.run(debug=True, port=5000)