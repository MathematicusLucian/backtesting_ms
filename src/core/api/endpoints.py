# -*- coding: utf-8 -*-
# from datetime import datetime, timedelta
# from functools import wraps
# from hashlib import sha1, md5
from jinja2 import TemplateNotFound
from markupsafe import escape
from flask import abort, app, Blueprint, jsonify, redirect, render_template, abort, request, url_for
# from flask import (_request_ctx_stack, abort, current_app, flash, redirect,
#                    request, session, url_for)
from flask.ext.cache import Cache
# from flask.ext.login import login_required, current_user
# from flask.signals import Namespace
# from werkzeug.local import LocalProxy
# from werkzeug.security import safe_str_cmp
# from werkzeug.urls import url_decode, url_encode
from src.utils.common import get_config
# from src.models import Backtest
cache = Cache(app)

# if sys.version < '3':  # pragma: no cover
#     from urlparse import urlparse, urlunparse
# else:  # pragma: no cover
#     from urllib.parse import urlparse, urlunparse
#     unicode = str
# _signals = Namespace()
# current_user = LocalProxy(lambda: _get_user() or
#                           current_app.login_manager.anonymous_user())
# COOKIE_NAME = 'remember_token'
# COOKIE_DURATION = timedelta(days=365)
# COOKIE_SECURE = None
# COOKIE_HTTPONLY = False
# LOGIN_MESSAGE = u'Please log in to access this page.'
# LOGIN_MESSAGE_CATEGORY = 'message'
# REFRESH_MESSAGE = u'Please reauthenticate to access this page.'
# REFRESH_MESSAGE_CATEGORY = 'message'
# api_key = get_config('')
backtesting_bp = Blueprint('backtesting_bp', __name__,
    template_folder='templates')
# backtesting_bp = Blueprint('backtesting_bp', __name__,
#     template_folder='templates',
#     static_folder='static', static_url_path='assets')
# user_logged_in = _signals.signal('logged-in')
# user_logged_out = _signals.signal('logged-out')
# user_loaded_from_cookie = _signals.signal('loaded-from-cookie')
# user_login_confirmed = _signals.signal('login-confirmed')
# user_unauthorized = _signals.signal('unauthorized')
# user_needs_refresh = _signals.signal('needs-refresh')
# session_protected = _signals.signal('session-protected')

@backtesting_bp.errorhandler(404)
def not_found():
    return redirect(url_for('not_found'))

@backtesting_bp('/not-found')
def page_not_found(error):
    return render_template('pages/404.html')
    # abort(404)

@backtesting_bp.errorhandler(405)
def handle_api_error(ex):
    if request.path.startswith('/api/'):
        return jsonify(error=str(ex)), ex.code
    else:
        return ex

# --------------------
# ------- ROOT -------
# --------------------    
# http://127.0.0.1:5000/
@backtesting_bp.route("/", defaults={'page': 'index'})
@backtesting_bp.route("/api")
@backtesting_bp.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)

@backtesting_bp.route("/api/ping")
@cache.cached(timeout=60)
def ping():
    return jsonify({"status": 200, "msg":"You pinged the Backtesting API"})

# -------------------------
# ------- DASHBOARD -------
# -------------------------    
# @backtesting_bp.route('/dashboard')
# @login_required
# def account():
#     return render_template("account.html")