from django.contrib.sessions.backends.db import SessionStore
from account.models import User


def get_account(type: str, data):
    status = False
    r = {"error": "未知错误"}
    if type == "PWD":
        account = login_account_by_pwd(data["email"], encrypt_password(data["password"]))
        if account is not None:
            t = SessionStore()
            t["id"] = account.id
            t["email"] = account.email
            t["password"] = account.password
            t.create()
            r = {"session": t.session_key, "email": account.email}
            status = True
        else:
            r = {"error": "邮箱或密码错误"}
    elif type == "SESSION":
        account = login_account_by_session(data["session"])
        if account is not None:
            r = {"session": data["session"], "email": account.email}
            status = True
        else:
            r = {"error": "session无效"}
    return [r, status]


def login_account_by_pwd(email, password):
    try:
        return User.objects.filter(email=email, password=password)[0]
    except:
        return None


def login_account_by_session(session: str):
    try:
        data = SessionStore(session_key=session)
        return login_account_by_pwd(data["email"], data["password"])
    except:
        return None


def get_user_by_session(session: str):
    r = None
    try:
        data = SessionStore(session_key=session)
        account = login_account_by_pwd(data["email"], data["password"])
        if account is not None:
            r = account.id
    except:
        pass
    return r


def get_account_by_email(email: str):
    try:
        return User.objects.filter(email=email)[0]
    except:
        return None


def creat_account(email: str, password: str):
    try:
        if email == "" or password == "":
            return [{"error": "必要参数为空"}, False]
        if get_account_by_email(email) is not None:
            return [{"error": "邮箱已被注册"}, False]
        password=encrypt_password(password)
        account = User.objects.create(email=email, password=password)
        t = SessionStore()
        t["id"] = account.id
        t["email"] = account.email
        t["password"] = account.password
        t.create()
        return [{"session": t.session_key, "email": account.email}, True]
    except Exception as e:
        return [{"error": str(e)}, False]


def encrypt_password(password: str):
    '''
    加密密码
    :param password:
    :return:
    '''
    import hashlib
    from django.conf import settings
    m = hashlib.sha256(settings.SECRET_KEY.encode())
    m.update(password.encode())
    return m.hexdigest()
