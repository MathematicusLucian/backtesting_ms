from unicodedata import *
from numpy import unicode_

class UserMixin(object):
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode_(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal
    
class AnonymousUserMixin(object):
    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    def is_anonymous(self):
        return True

    def get_id(self):
        return