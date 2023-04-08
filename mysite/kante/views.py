from django.shortcuts import render
from django.http import HttpResponse
from .models import MyModel
from django.views.decorators.csrf import csrf_exempt

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

        context = {'value' : content}

        return render(request, 'test.html', context)