from django.urls import path
from .views import rule_info

urlpatterns = [
    path('rules', rule_info),
]
