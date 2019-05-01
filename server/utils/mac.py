"""Represents MAC addresses in the application
"""
class Mac():

    def __init__(self, mac_addr):
        self.mac_addr = mac_addr
        if not ':' in self.mac_addr:
            self.mac_addr = self._normalize()

    def __str__(self):
        return self.mac_addr

    def minify(self):
        return self.mac_addr.replace(':', '')

    def _normalize(self):
        # Assuming valid minified mac address
        if ':' in self.mac_addr:
            return self.mac_addr
        
        return ':'.join(a + b for a, b in zip(self.mac_addr[::2], self.mac_addr[1::2]))