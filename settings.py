import os

SECRET_KEY = b'12345678901234567890123456789012'
# TODO replace with safe key on deployment
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
