"""Util class for encrypting given data, use as Encrypter('data', 'secret').encrypt()
"""
import pyffx

class Encrypter():

    def __init__(self, data, secret):
        self.data = data
        self.e = pyffx.String(bytes(secret), len(data))

    def encrypt(self):
        return e.encrypt(self.data)

    def decrypt(self):
        return e.decrypt(self.data)