from django.http import HttpResponse
from pysnmp.hlapi import *
from django.shortcuts import render
from .template import *

def snmp_view(request):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget(('demo.snmplabs.com', 161)),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
    )

    if errorIndication:
        return HttpResponse(errorIndication)
    elif errorStatus:
        return HttpResponse('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        result = []
        for varBind in varBinds:
            result.append(' = '.join([x.prettyPrint() for x in varBind]))
        return HttpResponse(result)
    
def snmp_info(request):
    # SNMP 정보 가져오기
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget(('demo.snmplabs.com', 161)),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
    )
    # 가져온 정보 Context 변수에 저장
    context = {}
    if varBinds:
        context['sys_descr'] = varBinds[0][1]
    return render(request, 'snmp_info.html', context)  