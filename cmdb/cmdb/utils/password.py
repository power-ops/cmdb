from random import sample
from django.conf import settings
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import base64

password_list = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=',
]

crypt_sm4 = CryptSM4()


def gen(leng=16):
    return "".join(sample(password_list, leng)).replace(' ', '')


def encrypt_ecb(password):
    crypt_sm4.set_key(settings.SECRET_KEY.encode(), SM4_ENCRYPT)
    return base64.b64encode(crypt_sm4.crypt_ecb(password.encode())).decode("utf-8")


def decrypt_ecb(encrypted_password):
    crypt_sm4.set_key(settings.SECRET_KEY.encode(), SM4_DECRYPT)
    return crypt_sm4.crypt_ecb(base64.b64decode(encrypted_password)).decode("utf-8")


def encrypt_cbc(password):
    crypt_sm4.set_key(settings.SECRET_KEY.encode(), SM4_ENCRYPT)
    return base64.b64encode(crypt_sm4.crypt_cbc(settings.SM4_VI.encode(), password.encode())).decode("utf-8")


def decrypt_cbc(encrypted_password):
    crypt_sm4.set_key(settings.SECRET_KEY.encode(), SM4_DECRYPT)
    return crypt_sm4.crypt_cbc(settings.SM4_VI.encode(), base64.b64decode(encrypted_password)).decode("utf-8")

# def encrypt(rsa_public_key, password):
#     public_key = RSA.importKey(rsa_public_key.encode())
#     crypto = rsa.encrypt(password.encode(), public_key)
#     crypto = base64.b64encode(crypto)
#     return crypto
