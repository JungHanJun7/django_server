from django.db import models

# Create your models here.
class Pogba(models.Model):
    public_ip = models.CharField(max_length=255)
    private_ip = models.GenericIPAddressField(default="127.0.0.1")

