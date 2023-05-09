
# import os
# import glob

# folder_path = r"\\192.168.0.9\Snort\preproc_rules"
# file_extension = '*.rules'  # 파일 확장자

# # 폴더 내의 모든 파일 경로 가져오기
# files = glob.glob(os.path.join(folder_path, file_extension))

# content = ''

# for file in files:
#     try:
#         with open(file, 'r') as file:
#             content = file.read()
#     except FileNotFoundError:
#         print("File not found. Please check the file path and ensure the network drive is connected.")

#     for i in content.split('\n'):
#         print(i)
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from pysnmp.hlapi import *



HOST = "192.168.0.9"   # 접속할 장비의 IP 입력할 것
PORT = 161
COMMUNITY = "public"  # 접속할 장비의 community 정보 입력할 것

# text_data = '1.3.6.1.2.1.2.2.1.16.11,1.3.6.1.2.1.2.2.1.10.11'
text_data = '1.3.6.1.2.1.2.2.1.5.11,1.3.6.1.2.1.2.2.1.16.11'
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

a = []
for i in result.split(','):
    a.append(int(i))
print(a[1]/a[0])

