import uuid as uuid_modual
import secrets
import string
import random


def hex(length):
    return secrets.token_hex(length)

def uuid():
    return uuid_modual.uuid4()

def custom(length, low=False,up=True,numbers=True,symbols=False,custom:list=None):
    if not custom:
        chars = []
        if low:
            chars = chars + list(string.ascii_lowercase)
        if up:
            chars = chars + list(string.ascii_uppercase)
        if numbers:
            chars = chars + list(string.digits)
        if symbols:
            chars = chars + list(string.punctuation)
    else:
        chars = custom
    return "".join([random.choice(chars) for x in range(length)])