from django.urls import path
from .views import user_list
from . import views

urlpatterns = [
    path('datas/', user_list),
    path('tcphdrs/', views.tcphdr_list, name='tcphdr_list'),
    path('changes/', views.database_changes),
]
