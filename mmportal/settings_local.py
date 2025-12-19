from pathlib import Path

import os

SECRET_KEY = os.environ.get("SECRET_KEY", 'MM-(efny!yx+*ovmuxe_o%ft**5ejs4!tulw_hr79pbjv9m7z+)_d')
DEBUG = int(os.environ.get("DEBUG", default=1))
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ["http://*"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.mysql"),
        "NAME": os.environ.get("SQL_DATABASE", 'mmportal'),
        "USER": os.environ.get("SQL_USER", "root"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "24Oct12Aug"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"}
    }

}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
import pymysql

pymysql.install_as_MySQLdb()
