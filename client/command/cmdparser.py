class CommandParser:

    def __init__(self, response):
        self.response = response

    def parse(self):
        if not response.haslayer('DNS'):
            return None

        an = response['DNS']
        if an.type != 'TXT' # hardcoded for now
            return None

        if an.qname != "cp501-prod.do.dsp.microsoft.com": # hardcoded for now
            return None
        
        return an.rdata