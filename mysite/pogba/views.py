from django.shortcuts import render
from rest_framework.decorators import api_view
from pysnmp.hlapi import *

from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt  
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import socket
import struct


from django.db import connection

from django.db import connection

def alert(request):
    # 클라이언트가 GET 메소드로 요청한 경우
    if request.method == 'GET':
        context = {}

        # Django의 DB connection을 사용하여 cursor 객체 생성
        with connection.cursor() as cursor:
            # tcphdr 테이블과 event 테이블에서 필요한 column을 선택, cid가 같은 행을 선택
            cursor.execute("""
            SELECT t.sid, t.cid, t.tcp_sport, t.tcp_dport, t.tcp_seq, t.tcp_ack, t.tcp_flags, e.timestamp
            FROM tcphdr t
            JOIN event e ON t.cid = e.cid
            """)
            tcp_results = cursor.fetchall()
        # 각 행의 요소를 문자열로 변환하고, 공백으로 연결
        tcp_str = [' '.join(map(str, result)) for result in tcp_results]
         # 결과를 반전 (가장 최근의 이벤트가 위에 오도록)
        tcp_str.reverse()
        # 각 행을 개행 문자로 연결하고, 이를 컨텍스트 변수에 저장
        context['tcp'] = '\n'.join(tcp_str)

        # UDP에 대한 정보를 가져오는 쿼리를 실행하고 그 결과를 context에 저장
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT t.sid, t.cid, t.udp_sport, t.udp_dport, e.timestamp
            FROM udphdr t
            JOIN event e ON t.cid = e.cid
            """)
            udp_results = cursor.fetchall()

        udp_str = [' '.join(map(str, result)) for result in udp_results]
        udp_str.reverse()
        context['udp'] = '\n'.join(udp_str)

        # ICMP 대한 정보를 가져오는 쿼리를 실행하고 그 결과를 context에 저장
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT t.sid, t.cid, t.icmp_type, e.timestamp
            FROM icmphdr t
            JOIN event e ON t.cid = e.cid
            """)
            icmp_results = cursor.fetchall()

        icmp_str = [' '.join(map(str, result)) for result in icmp_results]
        icmp_str.reverse()
        context['icmp'] = '\n'.join(icmp_str)
    # IP 대한 정보를 가져오는 쿼리를 실행하고 그 결과를 context에 저장
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT t.sid, t.cid, t.ip_src, t.ip_dst, ip_ttl, e.timestamp
        FROM iphdr t
        JOIN event e ON t.cid = e.cid
        """)
        ip_results = cursor.fetchall()

        # ip_src 와 ip_dst 는 숫자로 되어 있으므로, 이를 사람이 읽기 쉬운 형태로 변환
        ip_str = []
        for result in ip_results:
            ip_src_dec = result[2]  # Assuming ip_src is at index 2
            ip_dst_dec = result[3]  # Assuming ip_dst is at index 3
            ip_src = socket.inet_ntoa(struct.pack('!L', ip_src_dec))
            ip_dst = socket.inet_ntoa(struct.pack('!L', ip_dst_dec))
            ip_str.append(' '.join(map(str, (result[0], result[1], ip_src, ip_dst, result[4], result[5]))))

        ip_str.reverse()
        context['ip'] = '\n'.join(ip_str)


        return render(request, "alert.html", context)




@csrf_exempt
def postTest(request):
    if request.method == 'GET':
        # GET 요청을 처리하는 코드
        return render(request, "ip_input.html")

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
    else :
        return render(request, "socket_test.html")

