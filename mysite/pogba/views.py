from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Pogba
from .serializers import PogbaSerializer
import random
from pysnmp.hlapi import *

# Create your views here.
@api_view(['GET'])
def helloAPI(request) :
    return Response("hello world!")

@api_view(['GET'])
def randomPogba(request, id) :
    HOST = "192.168.0.9"   # 접속할 장비의 IP 입력할 것
    PORT = 161
    COMMUNITY = "public"  # 접속할 장비의 community 정보 입력할 것


    engine = SnmpEngine()
    host = UdpTransportTarget((HOST, PORT))
    community = CommunityData(COMMUNITY, mpModel=1)
    identity_obj_list = [
            ObjectType(ObjectIdentity('1.3.6.1.2.1.6.6.0')),
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
                    return Response(str(varBinds[-1]))

    # data = {
    #     'data':id
    # }
    # return Response(data)
    # totalPogbas = Pogba.objects.all()
    # randomPogbas = random.sample(list(totalPogbas), id)
    # serializer = PogbaSerializer(randomPogbas, many=True)
    # return Response(serializer.data)

@api_view(['POST'])
def postTest(request):
    title = request.data.get('title')
    body = request.data.get('body')
    answer = request.data.get('answer')
    data={
        'title':title,
        'body': body,
        'answer':answer
    }
    return Response(data) 

def testing(request):
    return render(request, "socket_test.html")