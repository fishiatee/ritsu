import os

def gen_hex_str(length: int = 8):
    return os.urandom(length).hex()