"""Util class for encrypting given data, use as Encrypter('data', 'secret').encrypt()
"""
import pyffx

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-'
SPACE_SEQ = 'sp' # Since we cannot have spaces in the URL, we need to encode it with some alphanumeric sequence

class Encrypter():

    def __init__(self, data, secret):
        self.data = data
        self.alpha_string = self.get_alpha_str(data)
        self.e = pyffx.String(bytes(secret, 'utf-8'), ALPHABET, len(self.alpha_string))

    def encrypt(self):
        """Encrypts the given payload
        
        Returns:
            string -- encrypted data
        """

        encrypted = self.e.encrypt(self.alpha_string)
        return self.zip_encrypt(self.data, encrypted)

    def decrypt(self):
        """Decrypts the given payload
        
        Returns:
            string -- decrypted data
        """

        decrypted = self.e.decrypt(self.alpha_string)
        return self.zip_decrypt(self.data, decrypted)

    def get_alpha_str(self, original):
        """Removes non-alphanumeric characters from given string
        
        Arguments:
            original {string} -- the string data to be filtered
        
        Returns:
            string -- string with special chars stripped out
        """
        s = original.replace(' ', SPACE_SEQ)
        s = ''.join([c for c in s if c.isalnum()])
        return s

    def zip_encrypt(self, original, alpha):
        """Re-inserts special chars into given string given mapping of original string
        
        Arguments:
            original {string} -- the original string data
            alpha {string} -- alphanumeric version of teh string
        
        Returns:
            string -- encrypted version of string with special chars
        """

        s = ''
        original = original.replace(' ', SPACE_SEQ)
        alpha_index = 0
        for c in original:
            if c.isalnum():
                # Char is alphanumeric, should be encrypted correctly
                s += alpha[alpha_index]
                alpha_index += 1
            else:
                # Non-alphanumeric char, append to s
                s += c

        return s

    def zip_decrypt(self, original, alpha):
        """Re-inserts special chars into decrypted payload given mapping with original string
        
        Arguments:
            original {string} -- the original string data
            alpha {string} -- alphanumeric version of the string
        
        Returns:
            string -- decrypted string with special chars
        """

        s = ''
        alpha_index = 0
        for c in original:
            if c.isalnum():
                # Char is alphanumeric, should be encrypted correctly
                s += alpha[alpha_index]
                alpha_index += 1
            else:
                # Non-alphanumeric char, append to s
                s += c

        # Replace SPACE_SEQ with space char
        s = s.replace(SPACE_SEQ, ' ')
        return s

