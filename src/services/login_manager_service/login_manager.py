from flask import (_request_ctx_stack, abort, current_app, flash, redirect,
                   request, session, url_for)
from flask_login import current_user, session_protected, user_loaded_from_cookie, user_needs_refresh, user_unauthorized
from datetime import datetime
import warnings
from src.services.login_manager_service.login_utils import _create_identifier, _get_user, _user_context_processor, decode_cookie, encode_cookie, login_url, logout_user
from src.services.login_manager_service.user_mixin import AnonymousUserMixin

class LoginManager(login_msg, login_msg_cat, refresh_msg, refresh_msg_cat, object): # type: ignore
    def __init__(self,login_msg, login_msg_cat, refresh_msg, refresh_msg_cat, cookie_name, cookie_duration, cookie_secure, cookie_httponly, app=None, add_context_processor=True):
        self.anonymous_user = AnonymousUserMixin
        self.login_view = None
        self.login_message = login_msg
        self.login_message_category = login_msg_cat
        self.refresh_view = None
        self.needs_refresh_message = refresh_msg
        self.needs_refresh_message_category = refresh_msg_cat
        self.session_protection = 'basic'
        self.token_callback = None
        self.user_callback = None
        self.unauthorized_callback = None
        self.needs_refresh_callback = None
        self.cookie_name = cookie_name
        self.cookie_duration = cookie_duration
        self.cookie_secure = cookie_secure
        self.cookie_httponly = cookie_httponly
        if app is not None:
            self.init_app(app, add_context_processor)

    def setup_app(self, app, add_context_processor=True):  
        warnings.warn('Warning setup_app is deprecated. Please use init_app.',
            DeprecationWarning)
        self.init_app(app, add_context_processor)

    def init_app(self, app, add_context_processor=True):
        app.login_manager = self
        app.before_request(self._load_user)
        app.after_request(self._update_remember_cookie)
        self._login_disabled = app.config.get('LOGIN_DISABLED',
            app.config.get('TESTING', False))
        if add_context_processor:
            app.context_processor(_user_context_processor)

    def unauthorized(self):
        user_unauthorized.send(current_app._get_current_object())
        if self.unauthorized_callback:
            return self.unauthorized_callback()
        if not self.login_view:
            abort(401)
        if self.login_message:
            flash(self.login_message, category=self.login_message_category)
        return redirect(login_url(self.login_view, request.url))

    def user_loader(self, callback):
        self.user_callback = callback
        return callback

    def token_loader(self, callback):
        self.token_callback = callback
        return callback

    def unauthorized_handler(self, callback):
        self.unauthorized_callback = callback
        return callback

    def needs_refresh_handler(self, callback):
        self.needs_refresh_callback = callback
        return callback

    def needs_refresh(self):
        user_needs_refresh.send(current_app._get_current_object())
        if self.needs_refresh_callback:
            return self.needs_refresh_callback()
        if not self.refresh_view:
            abort(403)
        flash(self.needs_refresh_message,
              category=self.needs_refresh_message_category)
        return redirect(login_url(self.refresh_view, request.url))

    def reload_user(self):
        ctx = _request_ctx_stack.top
        user_id = session.get('user_id')
        if user_id is None:
            ctx.user = self.anonymous_user()
        else:
            user = self.user_callback(user_id)
            if user is None:
                logout_user()
            else:
                ctx.user = user

    def _load_user(self):
        config = current_app.config
        if config.get('SESSION_PROTECTION', self.session_protection):
            deleted = self._session_protection()
            if deleted:
                self.reload_user()
                return
        cookie_name = config.get('REMEMBER_COOKIE_NAME', self.cookie_name)
        if cookie_name in request.cookies and 'user_id' not in session:
            return self._load_from_cookie(request.cookies[cookie_name])
        return self.reload_user()

    def _session_protection(self):
        sess = session._get_current_object()
        ident = _create_identifier()
        if '_id' not in sess:
            sess['_id'] = ident
        elif ident != sess['_id']:
            app = current_app._get_current_object()
            mode = app.config.get('SESSION_PROTECTION', self.session_protection)
            if mode == 'basic' or sess.permanent:
                sess['_fresh'] = False
                session_protected.send(app)
                return False
            elif mode == 'strong':
                sess.clear()
                sess['remember'] = 'clear'
                session_protected.send(app)
                return True
        return False

    def _load_from_cookie(self, cookie):
        if self.token_callback:
            user = self.token_callback(cookie)
            if user is not None:
                session['user_id'] = user.get_id()
                session['_fresh'] = False
                _request_ctx_stack.top.user = user
            else:
                self.reload_user()
        else:
            user_id = decode_cookie(cookie)
            if user_id is not None:
                session['user_id'] = user_id
                session['_fresh'] = False

            self.reload_user()
            app = current_app._get_current_object()
            user_loaded_from_cookie.send(app, user=_get_user())

    def _update_remember_cookie(self, response):
        if 'remember' in session:
            operation = session.pop('remember', None)

            if operation == 'set' and 'user_id' in session:
                self._set_cookie(response)
            elif operation == 'clear':
                self._clear_cookie(response)
        return response

    def _set_cookie(self, response):
        config = current_app.config
        cookie_name = config.get('REMEMBER_COOKIE_NAME', self.cookie_name)
        duration = config.get('REMEMBER_COOKIE_DURATION', self.cookie_duration)
        domain = config.get('REMEMBER_COOKIE_DOMAIN')
        secure = config.get('REMEMBER_COOKIE_SECURE', self.cookie_secure)
        httponly = config.get('REMEMBER_COOKIE_HTTPONLY', self.cookie_httponly)
        if self.token_callback:
            data = current_user.get_auth_token()
        else:
            data = encode_cookie(str(session['user_id']))
        expires = datetime.utcnow() + duration
        response.set_cookie(cookie_name,
            value=data,
            expires=expires,
            domain=domain,
            secure=secure,
            httponly=httponly)

    def _clear_cookie(self, response):
        config = current_app.config
        cookie_name = config.get('REMEMBER_COOKIE_NAME', self.cookie_name)
        domain = config.get('REMEMBER_COOKIE_DOMAIN')
        response.delete_cookie(cookie_name, domain=domain)