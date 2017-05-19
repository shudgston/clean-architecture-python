"""
from links.lib.security import PASSWORD_CTX

hash = PASSWORD_CTX.encrypt('123')

PASSWORD_CTX.verify('123', hash)
>>> True
"""
from passlib.context import CryptContext


CONTEXT = {
    'PASSWORD_CTX': CryptContext(
        schemes=['pbkdf2_sha256'],
        default='pbkdf2_sha256',
        pbkdf2_sha256__default_rounds=100000)
}


def lower_rounds():
    """For unit testing (less rounds, faster)"""
    CONTEXT['PASSWORD_CTX'] = CryptContext(
        schemes=['pbkdf2_sha256'],
        default='pbkdf2_sha256',
        pbkdf2_sha256__default_rounds=1)


def create_password_hash(password):
    """
    """
    return CONTEXT['PASSWORD_CTX'].hash(password)


def check_password(password, password_hash):
    """
    """
    try:
        verified = CONTEXT['PASSWORD_CTX'].verify(password, password_hash)
    except TypeError:
        verified = False
    except ValueError:
        verified = False

    return verified
