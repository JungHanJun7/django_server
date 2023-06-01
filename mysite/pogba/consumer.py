import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django
django.setup()


from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from pysnmp.hlapi import *
from channels.layers import get_channel_layer
from .models import event

class SnmpConsumer(WebsocketConsumer):
    private_ip = None
    public_ip = None
    previous_event_count = event.objects.all().count()

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        # client로부터 수신한 문자열을 ','를 기준으로 분리하여 리스트로 변환
        temp = list(text_data.split(','))

        # 수신한 문자열이 IP라면, 이를 public IP로 설정
        if temp[0].count('.') == 3:
            self.public_ip = temp[0]

        # 수신한 문자열이 OID라면, SNMP 통신을 위한 설정 시작
        elif temp[0].count('.') > 3:
            # SNMP 통신을 위한 HOST와 PORT 설정
            HOST = self.public_ip
            PORT = 161
            COMMUNITY = "public"

            result = ''
            # SNMP 엔진 생성
            engine = SnmpEngine()
            # SNMP 통신 대상 주소 설정
            host = UdpTransportTarget((HOST, PORT))
            # SNMP 커뮤니티 데이터 설정
            community = CommunityData(COMMUNITY, mpModel=1)

            identity_obj_list = []
            # text_data를 ','를 기준으로 분리하고, 각 항목을 ObjectIdentity로 변환하여 리스트에 추가
            for i in text_data.split(','):
                identity_obj_list.append(ObjectType(ObjectIdentity(i)))

            # 리스트에 있는 각 ObjectIdentity에 대해서 SNMP getCmd를 수행
            for identity_obj in identity_obj_list:
                iterator = getCmd(engine, community, host, ContextData(), identity_obj)
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

                # SNMP 엔진 오류 처리
                if errorIndication:
                    print(errorIndication)
                else:
                    # SNMP 에이전트 오류 처리
                    if errorStatus:
                        print('%s at %s' % (errorStatus.prettyPrint(),
                            varBinds[int(errorIndex) - 1] if errorIndex else '?'))
                    else:
                        # SNMP 응답 내용 처리
                        string = str(varBinds[-1]).split()[-1]
                        result = result + string + ','
            # 마지막에 추가된 ',' 제거
            result = result[:-1]
            # 결과를 송신
            self.send(text_data=result)

        else :
            # 현재 event 객체의 개수를 저장
            current_event_count = event.objects.all().count()
            # 이전 event 객체 개수와 현재 event 객체 개수를 비교하여 변경사항이 있는지 확인
            if self.previous_event_count != current_event_count:
                self.previous_event_count = current_event_count
                self.send(text_data=str('변경O'))
            else :
                self.send(text_data=str('변경X'))
            
