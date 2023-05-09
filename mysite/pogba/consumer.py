from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from pysnmp.hlapi import *
from channels.layers import get_channel_layer


class SnmpConsumer(WebsocketConsumer):
    private_ip = None
    public_ip = None

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        temp = list(text_data.split(','))
        if temp[0].count('.') == 3 :
            self.public_ip = temp[0]
            self.private_ip = temp[1]
        else :
            HOST = self.public_ip  # 접속할 장비의 IP 입력할 것
            PORT = 161
            COMMUNITY = "public"  # 접속할 장비의 community 정보 입력할 것

            result = ''
            engine = SnmpEngine()
            host = UdpTransportTarget((HOST, PORT))
            community = CommunityData(COMMUNITY, mpModel=1)
            # identity_obj_list = [
            #     ObjectType(ObjectIdentity(text_data.split(',')[0])),
            #     ObjectType(ObjectIdentity(text_data.split(',')[1])),
            # ]
            identity_obj_list = []

            for i in text_data.split(',') :
                identity_obj_list.append(ObjectType(ObjectIdentity(i)))
                
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
                            result = result + string + ','
            result = result[:-1]
            self.send(text_data=result)

