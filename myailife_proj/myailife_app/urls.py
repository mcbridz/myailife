from django.urls import path
from . import views

app_name = 'myailife'

urlpatterns = [
    path('', views.index, name='index'),

]
