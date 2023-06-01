from django.urls import path,re_path

from . import consumer

# 웹소켓 URL 패턴을 정의
websocket_urlpatterns = [
    re_path(r'^ws/snmp', consumer.SnmpConsumer.as_asgi()),
]