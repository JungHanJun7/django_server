from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import subprocess
import time

@csrf_exempt
def rule_info(request):
    def restart_snort():
        # Snort 프로세스를 찾아 종료합니다.
        os.system('taskkill /f /im snort.exe')
        
        # Snort가 완전히 종료되는 것을 기다립니다.
        time.sleep(5)
        
        # Snort를 다시 시작합니다.
        subprocess.Popen(['snort', '-c', 'C:\Snort\etc\snort.conf', '-l', 'C:\Snort\log', '-i', '2'])


    # my_models = MyModel.objects.all()
    if request.method == 'GET':
        file_path = r"\\192.168.0.9\Snort\rules\user.rules"
        content = ''

        try:
            with open(file_path, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            print("File not found. Please check the file path and ensure the network drive is connected.")

        context = {'user_rule' : content}


        return render(request, 'test.html', context)

    if request.method == 'POST':
        data = json.loads(request.body)
        motion = data.get('motion')
        action = data.get('action')
        protocol = data.get('protocol')
        ScrIP = data.get('ScrIP')
        ScrPort = data.get('ScrPort')
        direction = data.get('direction')
        DstIP = data.get('DstIP')
        DstPort = data.get('DstPort')
        option = data.get('option')


        rule = f"{action} {protocol} {ScrIP} {ScrPort} {direction} {DstIP} {DstPort} ({option})"+'\n'
        
        file_path = r"\\192.168.0.9\Snort\rules\user.rules"
        if motion == 'add':
            with open(file_path, 'a') as file:
                file.write(rule)
            restart_snort()
        else :
            with open(file_path, 'r') as file:
                lines = file.readlines()

            result = [line for line in lines if line != rule]

            with open(file_path, 'w') as file:
                file.writelines(result)

            restart_snort()
            return HttpResponse(result)


        return HttpResponse(rule)
    else:
        return HttpResponse('Invalid request')