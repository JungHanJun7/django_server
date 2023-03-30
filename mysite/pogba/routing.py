from django.urls import path,re_path

from . import consumer

websocket_urlpatterns = [
    #path('ws/snmp/', consumer.SnmpConsumer.as_asgi()),
    re_path(r'^ws/snmp', consumer.SnmpConsumer.as_asgi()),
]