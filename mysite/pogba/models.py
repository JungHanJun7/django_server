from django.db import models

# Create your models here.
class event(models.Model):
    cid = models.PositiveIntegerField(primary_key=True)  # Unsigned int field
    timestamp = models.DateTimeField()
    class Meta:
        db_table = 'event'
        managed = False


class Pogba(models.Model):
    public_ip = models.CharField(max_length=255)
    private_ip = models.GenericIPAddressField(default="127.0.0.1")

 