from django.db import models

# Create your models here.
class event(models.Model):
    # Unsigned int field, 즉 양의 정수 필드로 primary key인 'cid'를 정의
    cid = models.PositiveIntegerField(primary_key=True) 
    # Event 발생 시간을 나타내는 DateTime 필드인 'timestamp'를 정의합니다.
    timestamp = models.DateTimeField()
    # 이 클래스의 메타데이터를 정의합니다.
    class Meta:
        db_table = 'event'
        managed = False


class Pogba(models.Model):
    public_ip = models.CharField(max_length=255)
    private_ip = models.GenericIPAddressField(default="127.0.0.1")

 