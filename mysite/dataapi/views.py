from django.shortcuts import render
from django.http import HttpResponse
from .models import Rule, TCPHdr
from django.views.decorators.csrf import csrf_exempt

def user_list(request):
    if request.method == 'GET':
        # 데이터베이스에서 모든 규칙을 가져옵니다.
        rules = Rule.objects.all()

        # Rule 모델의 모든 필드를 가져옵니다.
        fields = Rule._meta.fields

        context = {
            'rules': rules,
            'fields': fields,
        }

        return render(request, 'database_status.html', context)
    

    # views.py
def tcphdr_list(request):
    tcphdrs = TCPHdr.objects.all()
    fields = TCPHdr._meta.fields

    context = {
        'tcphdrs': tcphdrs,
        'fields': fields,
    }

    return render(request, 'tcphdr_list.html', context)


def database_changes(request):
    return render(request, 'database_changes.html')