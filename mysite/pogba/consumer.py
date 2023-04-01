from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from pysnmp.hlapi import *

class SnmpConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        
        HOST = "192.168.0.9"   # 접속할 장비의 IP 입력할 것
        PORT = 161
        COMMUNITY = "public"  # 접속할 장비의 community 정보 입력할 것

        engine = SnmpEngine()
        host = UdpTransportTarget((HOST, PORT))
        community = CommunityData(COMMUNITY, mpModel=1)
        identity_obj_list = [
            ObjectType(ObjectIdentity(text_data)),
            #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
        ]

        for identity_obj in identity_obj_list:
            iterator = getCmd(engine, community, host, ContextData(), identity_obj)
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            if errorIndication:  # SNMP engine errors
                print(errorIndication)
            else:
                if errorStatus:  # SNMP agent errors
                    print('%s at %s' % (errorStatus.prettyPrint(),
                        varBinds[int(errorIndex)-1] if errorIndex else '?'))
                else:
                    for varBind in varBinds:  # SNMP response contents
                        print(' = '.join([x.prettyPrint() for x in varBind]))
                        # self.send(text_data=str(varBinds[-1]))
                        self.send(text_data)
