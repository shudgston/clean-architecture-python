"""
from links.lib.security import PASSWORD_CTX

hash = PASSWORD_CTX.encrypt('123')

PASSWORD_CTX.verify('123', hash)
>>> True
"""
from passlib.context import CryptContext

from links.logger import get_logger

LOGGER = get_logger(__name__)

CONTEXT = {
    'PASSWORD_CTX': CryptContext(
        schemes=['pbkdf2_sha256'],
        default='pbkdf2_sha256',
        all__vary_rounds=0.1,
        all__default_rounds=100000)
}


def set_testing_ctx():
    """For unit testing (less rounds, faster)"""
    CONTEXT['PASSWORD_CTX'] = CryptContext(
        schemes=['pbkdf2_sha256'],
        default='pbkdf2_sha256',
        all__vary_rounds=0.1,
        pbkdf2_sha256__default_rounds=10)


def create_password_hash(password):
    """
    """
    return CONTEXT['PASSWORD_CTX'].encrypt(password)


def check_password(password, password_hash):
    """
    """
    try:
        verified = CONTEXT['PASSWORD_CTX'].verify(password, password_hash)
    except ValueError as ex:
        LOGGER.exception(ex)
        verified = False

    return verified
