from django.contrib.auth.hashers import (
    BasePasswordHasher
)
from gmssl import sm3, func


class SM3PasswordHasher(BasePasswordHasher):
    algorithm = 'sm3'

    def encode(self, password, salt=None):
        return self.algorithm + "$" + sm3.sm3_hash(func.bytes_to_list(password.encode()))

    def verify(self, password, encoded):
        return encoded == self.encode(password)
