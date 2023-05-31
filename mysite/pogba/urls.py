from django.urls import path, include
from .views import postTest, testing#, alert

urlpatterns = [
    path("hello2/", postTest),
    path("socket/",testing),
    #path("alert/", alert),
]

