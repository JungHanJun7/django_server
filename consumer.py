from django.http import HttpResponse
from pysnmp.hlapi import *

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