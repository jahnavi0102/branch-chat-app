"""
ASGI config for branch_chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
import chat_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'branch_chat_app.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(chat_app.routing.websocket_urlpatterns),
})

