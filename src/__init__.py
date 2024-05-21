# # -*- coding: utf-8 -*-
# from flask import Blueprint, Flask, url_for
# from src.settings import config
# from src.utils.common import register_blueprints__generic
# # from src.utils.utils import save_dataframe
# # from src.services.db.db import create_connection, is_table

# # save_dataframe = save_dataframe
# # create_connection = create_connection
# # is_table = is_table
# # # market data
# # order_books = {}
# # instruments = {}
# # tickers_container = []
# # mark_px_container = []
# # # position management
# # balance_and_position_container = []
# # account_container = []
# # positions_container = []
# # # order management
# # orders_container = []

# # admin = Blueprint('admin', __name__, static_folder='static')
# # admin = Blueprint('admin', __name__, template_folder='templates')
# # url_for('admin.static', filename='style.css')

# icons_bp = Blueprint('icons_bp', __name__,
#     static_folder='static',
#     static_url_path='icons')

# charts_module_bp = Blueprint('charts_module_bp', __name__,
#     static_folder='services/chart_service',
#     static_url_path='charts')

# # with icons_bp.open_resource('static/icons') as f:
# #     code = f.read()

# # with charts_module_bp.open_resource('services/chart_service') as f:
# #     code = f.read()

# def create_app(config_type, package_name, package_path):
#     app = Flask(__name__, instance_relative_config=True)
#     # print('config[config_type]',config[config_type])
#     app_settings = config[config_type]
#     app.config.from_object(app_settings)
#     register_blueprints__generic(app, package_name, package_path)
#     app.register_blueprint(icons_bp, url_prefix='/icons')
#     app.register_blueprint(charts_module_bp, url_prefix='/charts')
#     # with app.open_resource('static') as f:
#     #     code = f.read()
#     return app