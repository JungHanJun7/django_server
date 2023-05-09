from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class Rule(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
    

# models.py


class TCPHdr(models.Model):
    sid = models.IntegerField(max_length=100, primary_key=True)
    cid = models.IntegerField(max_length=100)
    # tcphdr 테이블의 모든 필드를 여기에 추가하십시오.

    class Meta:
        db_table = 'tcphdr'
        managed = False


class MyModel(models.Model):
    # 필드 정의
    pass

@receiver([post_save, post_delete], sender=MyModel)
def notify_change(sender, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "changes",
        {
            'type': 'send_change',
            'text': "변경사항이 있습니다."
        }
    )


