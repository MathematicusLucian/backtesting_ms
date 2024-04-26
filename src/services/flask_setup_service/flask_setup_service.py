from datetime import datetime
from functools import wraps
from src.api.endpoints import route
from src.api.websockets import socketio
# https://github.com/miguelgrinberg/Flask-SocketIO-Chat
# https://medium.com/hackervalleystudio/weekend-project-part-2-turning-flask-into-a-real-time-websocket-server-using-flask-socketio-ab6b45f1d896

class FlaskSetupService(object):
    def __init__(self, app, test_config=None, config_type=None, package_name=None, package_path=None, **configs):
        self.app = app
        self.configs(**configs)

    def configs(self, **configs):
        # app_settings = config[config_type]
        # self.app.config.from_object(app_settings)
        for config, value in configs:
            self.app.config[config.upper()] = value
        # if self.app.config["DEBUG"] == True:
        #     self.app.config.from_object('config.DevConfig')
        # else:
        #     self.app.config.from_object('config.ProdConfig')
        # # self.app.config.from_mapping(
        # #     SECRET_KEY='dev',
        # #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        # # )
        # # if test_config is None:
        # #     # load the instance config, if it exists, when not testing
        # #     app.config.from_pyfile('config.py', silent=True)
        # # else:
        # #     # load the test config if passed in
        # #     app.config.from_mapping(test_config)
        # # ensure the instance folder exists
        # try:
        #     os.makedirs(app.instance_path)
        # except OSError:
        #     pass
        # # db = SQLAlchemy(app)
        # # migrate = Migrate(app, db)
        # # with app.app_context():
        # #     db.create_all()
        self.add_blueprint_routes()
        self.add_endpoint__websockets()

    def sock_setup(self):
        pass
        # self.sock = Sock()
        # self.sock.init_app(self.app)

    def add_blueprint_routes(self):
        self.app.register_blueprint(route)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def add_endpoint__websockets(self):
        socketio.init_app(self.app)

    # def check_expired(self, func):
    #     @wraps(func)
    #     def decorated_function(*args, **kwargs):
    #         if datetime.utcnow() > current_user.account_expires:
    #             flash("Your account has expired. Update your billing info.")
    #             return redirect(url_for('account_billing'))
    #         return func(*args, **kwargs)
    #     return decorated_function

    def run(self, **kwargs):
        self.app.run(**kwargs)
    
# Scraper = scrape_job_sites_bot
# save_dataframe = save_dataframe
# create_connection = create_connection
# is_table = is_table

# flask_config = get_config('FLASK_CONFIG')
# config = flask_config if flask_config!=None else 'default'
# application = create_app_blueprint(config)