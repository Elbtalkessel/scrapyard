import os

BASE_DIR = os.path.dirname(__file__)

PROXY_PATH = None
REFRESH_PROXY_EACH = 30  # seconds
USER_AGENTS_PATH = os.path.join(BASE_DIR, 'support', 'ualist')

PROXY_TYPE = os.getenv('PROXY_TYPE', 'SOCKS5')

LOG_LEVEL = 'INFO'
LOG_MAX_FILE_BYTES = 1 * 1024 * 1024
LOG_BACKUP_COUNT = 50
