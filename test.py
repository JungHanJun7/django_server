from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from pysnmp.hlapi import *

HOST = "192.168.0.9"   # 접속할 장비의 IP 입력할 것
PORT = 161
COMMUNITY = "public"  # 접속할 장비의 community 정보 입력할 것

result = ''
engine = SnmpEngine()
host = UdpTransportTarget((HOST, PORT))
community = CommunityData(COMMUNITY, mpModel=1)

#34
identity_obj_list = []
text_data = "1.3.6.1.2.1.4.3.0,1.3.6.1.2.1.4.8.0"

identity_obj_list.append(ObjectType(ObjectIdentity(text_data)))

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
                string = str(varBinds[-1]).split()[-1]
                print(string)
identity_obj_list.pop()

