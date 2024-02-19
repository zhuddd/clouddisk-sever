from django.contrib.sessions.backends.cache import SessionStore


def newKey(data: dict, expiration: int = 3600):
    s = SessionStore()
    for k in data:
        s[k] = data[k]
    s.set_expiry(expiration)
    s.create()
    return s.session_key

def getKey(session: str):
    s = SessionStore(session_key=session)
    return s