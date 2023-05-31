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
        subprocess.Popen(['snort', '-c', 'C:\Snort\etc\snort.conf', '-l', 'C:\Snort\log', '-i', '1'])


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
    
    # if request.method == 'GET':
    #     # 마운트된 폴더 경로로 수정
    #     file_path = "/mnt/myshare/Snort/rules/user.rules"
    #     content = ''

    #     try:
    #         # 파일을 열고 내용을 읽음
    #         with open(file_path, 'r') as file:
    #             content = file.read()
    #     except FileNotFoundError:
    #         # 파일이 발견되지 않은 경우, 에러 메시지 출력
    #         print("File not found. Please check the file path and ensure the network drive is connected.")

    #     # 읽은 내용을 컨텍스트 변수에 할당
    #     context = {'user_rule' : content}

    #     # 수정된 컨텍스트를 이용해 test.html 렌더링 후 반환
    #     return render(request, 'test.html', context)

    
    # if request.method == 'POST':
    #     # 클라이언트로부터 받은 데이터(request.body)를 JSON 형식으로 해석
    #     data = json.loads(request.body)
    #     # 각각의 필드는 data 딕셔너리에서 가져옴
    #     motion = data.get('motion')
    #     action = data.get('action')
    #     protocol = data.get('protocol')
    #     ScrIP = data.get('ScrIP')
    #     ScrPort = data.get('ScrPort')
    #     direction = data.get('direction')
    #     DstIP = data.get('DstIP')
    #     DstPort = data.get('DstPort')
    #     option = data.get('option')

    #     # 파일에 쓸 내용을 만들어서 'rule'에 저장
    #     rule = f"{action} {protocol} {ScrIP} {ScrPort} {direction} {DstIP} {DstPort} ({option})"+'\n'
        
    #     # 작업을 수행할 파일의 경로를 지정
    #     file_path = "/mnt/myshare/Snort/rules/user.rules"
        
    #     # motion이 'add'인 경우에는 rule을 파일에 추가하고, Snort를 재시작
    #     if motion == 'add':
    #         with open(file_path, 'a') as file:
    #             file.write(rule)
    #         restart_snort()
    #     else :
    #         # motion이 'add'가 아닌 경우(delete)에는 rule을 파일에서 제거하고, Snort를 재시작
    #         with open(file_path, 'r') as file:
    #             lines = file.readlines()

    #         # rule과 일치하지 않는 줄만 선택해서 'result'에 저장
    #         result = [line for line in lines if line != rule]

    #         # 파일에 'result'를 다시 쓴 후 Snort를 재시작
    #         with open(file_path, 'w') as file:
    #             file.writelines(result)

    #         restart_snort()
    #         # 결과를 클라이언트에게 전송
    #         return HttpResponse(result)





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