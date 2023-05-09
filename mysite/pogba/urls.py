from django.urls import path, include
from .views import postTest, testing

urlpatterns = [
    path("hello2/", postTest),
    path("socket/",testing),
]

