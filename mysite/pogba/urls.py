from django.urls import path, include
from .views import helloAPI, randomPogba, postTest, testing

urlpatterns = [
    path("hello/", helloAPI),
    path("<int:id>/", randomPogba),
    path("hello2/", postTest),
    path("socket/",testing),
    # path("cash/<int:message_id>/", get_cached_message)
]

