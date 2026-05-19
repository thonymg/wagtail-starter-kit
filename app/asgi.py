import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.base")

# Minimal ASGI config for Daphne.
# When Django Channels is added, wrap this with ProtocolTypeRouter here.
application = get_asgi_application()
