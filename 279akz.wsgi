import sys
import os

os.environ['APP_ENV'] = 'prod'

sys.path.append('/var/www/html/zeerak.net/public_html/279akz/system2share')

from server import app as application