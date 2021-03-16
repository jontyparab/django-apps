from django.urls import re_path
from . import consumers

ws_urlpatterns = [
    re_path(r'^apps/ws/chat/(?P<username>\w+)/$', consumers.ChatRoomConsumer.as_asgi())
]