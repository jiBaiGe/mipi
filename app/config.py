import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = '/tmp'

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:changeme@127.0.0.1:5432/mipi'
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['json' ])

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = b'_kjgkljs9024eck]/'

# Secret key for signing cookies
SECRET_KEY = b'_kjgkljs9024eck]/'


