import binascii
import os


def generate_jti():
    return binascii.hexlify(os.urandom(32)).decode()

