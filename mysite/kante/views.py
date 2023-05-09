from django.shortcuts import render
from django.http import HttpResponse
from .models import MyModel
from django.views.decorators.csrf import csrf_exempt
import os
import glob
import json

@csrf_exempt
def rule_info(request):
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

        folder_path = r"\\192.168.0.9\Snort\preproc_rules"
        file_extension = '*.rules'  # 파일 확장자 

        files = glob.glob(os.path.join(folder_path, file_extension))
        temp = ''

        for file in files:
            try:
                with open(file, 'r') as file:
                    content = file.read()
            except FileNotFoundError:
                print("File not found. Please check the file path and ensure the network drive is connected.")

            for i in content.split('\n'):
                temp = temp + i + '\n'
    
        context['default_rule'] = temp

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


        rule = f"{action} {protocol} {ScrIP} {ScrPort} {direction} {DstIP} {DstPort} ({option})"
        
        file_path = r"\\192.168.0.9\Snort\rules\user.rules"
        if motion == 'add':
            with open(file_path, 'a') as file:
                file.write(rule + "\n")
        else :
            with open(file_path, 'r') as file:
                lines = file.readlines()

            result = [line for line in lines if line != rule]

            with open(file_path, 'w') as file:
                file.writelines(result)

            return HttpResponse(result)


        return HttpResponse(rule)
    else:
        return HttpResponse('Invalid request')