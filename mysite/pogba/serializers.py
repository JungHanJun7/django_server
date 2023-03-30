from rest_framework import serializers
from .models import Pogba

class PogbaSerializer(serializers.ModelSerializer):
    class Meta :
        model = Pogba
        fields = ('title', 'body', 'answer')