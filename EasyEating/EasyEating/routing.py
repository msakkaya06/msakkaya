# myapp/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/business/(?P<business_id>\d+)/$', consumers.BusinessConsumer.as_asgi()),
    re_path(r'ws/desk/(?P<desk_slug>[-\w]+)/$', consumers.DeskConsumer.as_asgi()),
]
