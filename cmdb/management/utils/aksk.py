from django.contrib.sessions.backends.db import SessionStore
import uuid


def New(data):
    a = SessionStore()
    a['data'] = data
    a['sk'] = str(uuid.uuid4())
    a.set_expiry(600)
    a.create()
    return a.session_key, a['sk']


def Get(id):
    data = SessionStore(id)
    if not data.load():
        return None
    return data
