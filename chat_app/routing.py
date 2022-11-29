"""
All the routing of the apps are listed here. 
"""
from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:pk>/<int:user_id>', consumers.ChatConsumer.as_asgi()),
]
