"""Database models."""
from google.appengine.ext import ndb
from password import make_pw_hash
from password import valid_pw


def users_key(group='default'):
    key = ndb.Key('users', group)
    return key

class User(ndb.Model):
    """Database model for a user object."""
    name = ndb.StringProperty(required=True)
    hashed_pw = ndb.StringProperty(required=True)
    email = ndb.StringProperty()

    @classmethod
    def get_user_by_id(CLS, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def get_user_by_name(CLS, name):
        user = User.query(User.name == name).get()
        return user

    @classmethod
    def register(CLS, name, password, email=None):
        hashed_pw = make_pw_hash(name, password)
        return User(parent=users_key(),
                    name=name,
                    hashed_pw=hashed_pw,
                    email=email)

    @classmethod
    def user_login(CLS, name, password):
        user = CLS.get_by_name(name)
        if user and valid_pw(name, password, user.hashed_pw):
            return user
