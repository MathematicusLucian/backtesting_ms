# -*- coding: utf-8 -*-
import os
from src.api import create_app_blueprint
from src.utils.common import get_config

flask_config = get_config('FLASK_CONFIG')
config = flask_config if flask_config!=None else 'default'
# print('CFG',config)
application = create_app_blueprint(config)