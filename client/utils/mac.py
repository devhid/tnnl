# system imports
from uuid import getnode

def get_mac():
    return ''.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2)).lower() 