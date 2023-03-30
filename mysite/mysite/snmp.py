from pysnmp.hlapi import *

# SNMP 정보 설정
community_name = 'public'
ip_address = '127.0.0.1'
oid = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)

# SNMP 프로토콜 설정
snmp_engine = SnmpEngine()
community_data = CommunityData(community_name)
udp_transport_target = UdpTransportTarget((ip_address, 161))
context_data = ContextData()

# SNMP 요청 보내기
iterator = getCmd(snmp_engine, community_data, udp_transport_target, context_data, oid)
error_indication, error_status, error_index, var_binds = next(iterator)

# SNMP 응답 처리
if error_indication:
    print(error_indication)
else:
    for var_bind in var_binds:
        print(var_bind)