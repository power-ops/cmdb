from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
import base64
from gmssl import sm3, func
from django.utils.crypto import constant_time_compare, pbkdf2
from django.utils.translation import gettext_noop as _


class sm3digest(object):
    name = 'sm3'

    def __init__(self, __string=None):
        self.text = __string

    def hexdigest(self):
        return sm3.sm3_hash(func.bytes_to_list(self.text.encode()))


class PBKDF2SM3PasswordHasher(BasePasswordHasher):
    algorithm = 'pbkdf2_sm3'
    iterations = 180000

    def encode(self, password, salt, iterations=None):
        assert password is not None
        assert salt and '$' not in salt
        iterations = iterations or self.iterations
        hash = pbkdf2(password, salt, iterations, digest=sm3digest)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def verify(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt, int(iterations))
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return {
            _('algorithm'): algorithm,
            _('iterations'): iterations,
            _('salt'): mask_hash(salt),
            _('hash'): mask_hash(hash),
        }
