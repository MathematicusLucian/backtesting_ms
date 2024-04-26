from urllib.parse import urlparse, urlunparse
from flask import (_request_ctx_stack, abort, current_app, flash, redirect,
                   request, session, url_for)
from flask_login import current_user, user_logged_in, user_logged_out, user_login_confirmed
from numpy import unicode_
from werkzeug.security import safe_str_cmp
from werkzeug.urls import url_decode, url_encode
from functools import wraps
from hashlib import sha1, md5
import hmac
from src.services.login_manager_service.user_mixin import AnonymousUserMixin

def encode_cookie(payload):
    return u'{0}|{1}'.format(payload, _cookie_digest(payload))

def decode_cookie(cookie):
    try:
        payload, digest = cookie.rsplit(u'|', 1)
        if hasattr(digest, 'decode'):
            digest = digest.decode('ascii')
    except ValueError:
        return
    if safe_str_cmp(_cookie_digest(payload), digest):
        return payload

def make_next_param(login_url, current_url):
    l = urlparse(login_url)
    c = urlparse(current_url)

    if (not l.scheme or l.scheme == c.scheme) and (not l.netloc or l.netloc == c.netloc):
        return urlunparse(('', '', c.path, c.params, c.query, ''))
    return current_url

def login_url(login_view, next_url=None, next_field='next'):
    if login_view.startswith(('https://', 'http://', '/')):
        base = login_view
    else:
        base = url_for(login_view)
    if next_url is None:
        return base
    parts = list(urlparse(base))
    md = url_decode(parts[4])
    md[next_field] = make_next_param(base, next_url)
    parts[4] = url_encode(md, sort=True)
    return urlunparse(parts)

def make_secure_token(*args, **options):
    key = options.get('key')
    key = _secret_key(key)
    l = [s if isinstance(s, bytes) else s.encode('utf-8') for s in args]
    payload = b'\0'.join(l)
    token_value = hmac.new(key, payload, sha1).hexdigest()
    if hasattr(token_value, 'decode'): 
        token_value = token_value.decode('utf-8') 
    return token_value


def login_fresh():
    return session.get('_fresh', False)

def login_user(user, remember=False, force=False):
    if not force and not user.is_active():
        return False
    user_id = user.get_id()
    session['user_id'] = user_id
    session['_fresh'] = True
    if remember:
        session['remember'] = 'set'
    _request_ctx_stack.top.user = user
    user_logged_in.send(current_app._get_current_object(), user=_get_user())
    return True

def logout_user(cookie_name):
    if 'user_id' in session:
        session.pop('user_id')
    if '_fresh' in session:
        session.pop('_fresh')
    cookie_name = current_app.config.get('REMEMBER_COOKIE_NAME', cookie_name)
    if cookie_name in request.cookies:
        session['remember'] = 'clear'
    user = _get_user()
    if user and not user.is_anonymous():
        user_logged_out.send(current_app._get_current_object(), user=user)
    current_app.login_manager.reload_user()
    return True

def confirm_login():
    session['_fresh'] = True
    session['_id'] = _create_identifier()
    user_login_confirmed.send(current_app._get_current_object())

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated():
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

def fresh_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated():
            return current_app.login_manager.unauthorized()
        elif not login_fresh():
            return current_app.login_manager.needs_refresh()
        return func(*args, **kwargs)
    return decorated_view

def _get_user():
    return getattr(_request_ctx_stack.top, 'user', None)

def _cookie_digest(payload, key=None):
    key = _secret_key(key)
    return hmac.new(key, payload.encode('utf-8'), sha1).hexdigest()

def _get_remote_addr():
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is not None:
        address = address.encode('utf-8')
    return address

def _create_identifier():
    user_agent = request.headers.get('User-Agent')
    if user_agent is not None:
        user_agent = user_agent.encode('utf-8')
    base = '{0}|{1}'.format(_get_remote_addr(), user_agent)
    if str is bytes:
        base = unicode_(base, 'utf-8', errors='replace')
    h = md5()
    h.update(base.encode('utf8'))
    return h.hexdigest()

def _user_context_processor():
    return dict(current_user=_get_user())

def _secret_key(key=None):
    if key is None:
        key = current_app.config['SECRET_KEY']
    if isinstance(key, unicode_): 
        key = key.encode('latin1') 
    return key