from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Pogba
from .serializers import PogbaSerializer
from pysnmp.hlapi import *

from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from .models import Message
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt



# @api_view(['GET'])
# def randomPogba(request, id) :
#     HOST = "192.168.0.9"   # 접속할 장비의 IP 입력할 것
#     PORT = 161
#     COMMUNITY = "public"  # 접속할 장비의 community 정보 입력할 것


#     engine = SnmpEngine()
#     host = UdpTransportTarget((HOST, PORT))
#     community = CommunityData(COMMUNITY, mpModel=1)
#     identity_obj_list = [
#             ObjectType(ObjectIdentity('1.3.6.1.2.1.6.6.0')),
#             #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
#     ]

#     for identity_obj in identity_obj_list:
#         iterator = getCmd(engine, community, host, ContextData(), identity_obj)
#         errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
#         if errorIndication:  # SNMP engine errors
#             print(errorIndication)
#         else:
#             if errorStatus:  # SNMP agent errors
#                 print('%s at %s' % (errorStatus.prettyPrint(),
#                     varBinds[int(errorIndex)-1] if errorIndex else '?'))
#             else:
#                 for varBind in varBinds:  # SNMP response contents
#                     print(' = '.join([x.prettyPrint() for x in varBind]))
#                     return Response(str(varBinds[-1]))

    # data = {
    #     'data':id
    # }
    # return Response(data)
    # totalPogbas = Pogba.objects.all()
    # randomPogbas = random.sample(list(totalPogbas), id)
    # serializer = PogbaSerializer(randomPogbas, many=True)
    # return Response(serializer.data)

# @api_view(['POST'])
# def postTest(request):
#     public_ip = request.data.get('Public_IP')
#     private_ip = request.data.get('Private_IP')
#     data={
#         'public_ip':public_ip,
#         'private_ip': private_ip,
#     }
#     render(request, "ip_input.html")
#     return Response(data) 

@csrf_exempt
def postTest(request):
    if request.method == 'GET':
        # GET 요청을 처리하는 코드
        return render(request, "ip_input.html")

    # elif request.method == 'POST':
    #     # POST 요청을 처리하는 코드
    #     public_ip = request.data.get('public_ip')
    #     private_ip = request.data.get('private_ip')
    #     data={
    #         'public_ip':public_ip,
    #         'private_ip': private_ip,
    #     }
    #     return render(request, "./")
        # return Response(data) 


    else:
        # 지원되지 않는 요청 메서드에 대한 응답
        return HttpResponse(status=405)



from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def testing(request):
    if request.method == 'POST':
        public_ip = request.POST.get('public_ip')
        private_ip = request.POST.get('private_ip')
        initial_data = {'public_ip': public_ip, 'private_ip': private_ip}
        return render(request, "socket_test.html", initial_data)


# @api_view(['GET'])
# def get_cached_message(request, message_id):
#     cached_message = cache.get(f'message_{message_id}')
#     if cached_message is not None:
#         return JsonResponse({'status': 'success', 'public_ip': cached_message.public_ip, 'private_ip': cached_message.private_ip})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Data not found in cache'})

# @api_view(['GET'])
# def postTest(request):
#     # public_ip = request.data.get('Public_IP')
#     # private_ip = request.data.get('Private_IP')
#     public_ip = '127.0.0.1'
#     private_ip = '127.0.0.2'
#     data ={
#         'public_ip':public_ip,
#         'private_ip':private_ip
#     }

#     if data is not None:
#         response = JsonResponse({'status': 'success', 'message': 'Data saved in cookie'})
#         response.set_cookie('cookie_name', data, max_age=60 * 60 * 24)  # 쿠키 유효 시간을 1일로 설정
#         return response
#     else:
#         return JsonResponse({'status': 'error', 'message': 'No data provided'})
