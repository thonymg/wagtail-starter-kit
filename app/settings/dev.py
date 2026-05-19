import socket

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-i7bqh5eiw93f*$d6q_#$506gp%w8@xvo0nu77f_j&g&yt-zh38"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += [  # noqa F405
    "app.style_guide",
    "wagtail.contrib.styleguide",
    "django_browser_reload",
    "debug_toolbar",
    "django_extensions",
]

# debug_toolbar middleware must come first
MIDDLEWARE = [  # noqa F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE  # noqa F405

MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]  # noqa F405

# debug_toolbar only renders for IPs in INTERNAL_IPS.
# The socket lookup adds the Docker gateway IP automatically so it works
# both locally (127.0.0.1) and inside Docker containers.
_hostname, _, _ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = ["127.0.0.1"] + [ip[: ip.rfind(".")] + ".1" for ip in _ips]

# django-extensions: use IPython for shell_plus
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True

DJANGO_VITE["default"]["dev_mode"] = True  # noqa F405

try:
    from .local import *  # noqa
except ImportError:
    pass
