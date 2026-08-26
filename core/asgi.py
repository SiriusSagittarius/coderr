"""ASGI config for the core project."""
# 1. Standard library
import os

# 2. Third-party
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_asgi_application()
