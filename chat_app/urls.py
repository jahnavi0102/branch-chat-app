"""
All the urls of the apps are listed here.
"""
from django.urls import path
from .views import UserViewSet, MessageViewSet, room, ThreadViewSet

urlpatterns = [
    path('user/', UserViewSet.as_view({'post': 'create'})),
    path('user/<int:pk>/', UserViewSet.as_view({'delete': 'delete'})),
    path('message-list/', MessageViewSet.as_view({'get': 'list'})),
    path('send-message/', MessageViewSet.as_view({'post': 'create'})),
    path('thread-list/', ThreadViewSet.as_view({'get': 'list'})),
    path("<int:pk>/<int:user_id>", room, name="room"),
]
