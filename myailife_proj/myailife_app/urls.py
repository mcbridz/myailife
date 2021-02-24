from django.urls import path
from . import views

app_name = 'myailife'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_posts', views.getPosts, name='get_posts'),
]
