from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from django.db import connection
from models import MyModel

def database_has_changed():
    # 데이터베이스의 변화를 확인하기 위해 마지막으로 저장된 레코드 수를 저장하는 변수
    global last_record_count

    # 현재 테이블에 있는 레코드 수를 가져옵니다.
    current_record_count = MyModel.objects.count()

    # 마지막으로 저장된 레코드 수와 현재 레코드 수를 비교합니다.
    if current_record_count != last_record_count:
        # 레코드 수가 다른 경우, 데이터베이스에 변화가 있었다고 판단하고, last_record_count를 업데이트합니다.
        last_record_count = current_record_count
        return True

    return False

class Command(BaseCommand):
    help = 'Check for database changes and notify via WebSocket'


    def handle(self, *args, **options):
        channel_layer = get_channel_layer()

        while True:
            if database_has_changed():
                async_to_sync(channel_layer.group_send)(
                    'changes',
                    {
                        'type': 'send_change',
                        'message': '데이터베이스에 변화가 있습니다.'
                    }
                )
            else:
                async_to_sync(channel_layer.group_send)(
                    'changes',
                    {
                        'type': 'send_change',
                        'message': '데이터베이스에 변화가 없습니다.'
                    }
                )
            time.sleep(3)

    