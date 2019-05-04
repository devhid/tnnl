"""Util class for encrypting given data, use as Encrypter('data', 'secret').encrypt()
"""
import pyffx

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-'

def decrypt(data, secret):
    """Decrypts the given payload
    
    Returns:
        string -- decrypted data
    """

    decrypted = pyffx.String(bytes(secret), ALPHABET, len(_get_alpha_str(data)))
    return _zip_decrypt(data, decrypted)

def _get_alpha_str(original):
    """Removes non-alphanumeric characters from given string
    
    Arguments:
        original {string} -- the string data to be filtered
    
    Returns:
        string -- string with special chars stripped out
    """
    s = ''.join([c for c in original if c.isalnum()])
    return s

def _zip_decrypt(original, alpha):
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
    return s
