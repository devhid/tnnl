"""App constants"""

# Help Messages
HELP_CONFIG_PATH = 'Path to custom *.ini file containing config server/client settings.'

DEFAULT_CONFIG_PATH = 'config.ini'

# Defaults for Server
DEFAULT_SERVER_INTERFACE = 'eth0'
DEFAULT_DATA_DIR = './data' # Storage of exfiltrated data

# Defaults for Client
DEFAULT_CLIENT_PING_INTERVAL = '60' # Measured in minutes for checking commands on server
DEFAULT_CLIENT_DOMAIN = 'cp501-prod.do.dsp.microsoft.com' # Domain to spoof requests with
DEFAULT_CLIENT_CNAME = 'cp501-prod.dodsp.mp.microsoft.com.nsatc.net'

# Config files
CONFIG_SERVER = 'SERVER'
CONFIG_CLIENT = 'CLIENT'
CONFIG_SERVER_KEYS = ['interface', 'data_dir']
CONFIG_CLIENT_KEYS = ['client_ping_interval', 'client_domain', 'client_cname']

def default_server_conf():
    return {
        'interface': DEFAULT_SERVER_INTERFACE,
        'data_dir': DEFAULT_DATA_DIR
    }

def default_client_conf():
    return {
        'client_ping_interval': DEFAULT_CLIENT_PING_INTERVAL,
        'client_domain': DEFAULT_CLIENT_DOMAIN,
        'client_name': DEFAULT_CLIENT_CNAME
    }