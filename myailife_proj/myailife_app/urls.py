from django.urls import path
from . import views

app_name = 'myailife'

urlpatterns = [
    path('', views.index, name='index'),
    path('getPosts', views.getPosts, name='getPosts'),
    path('addPost', views.addPost, name='addPost'),
    path('deletePost', views.deletePost, name='deletePost'),
    path('getKey', views.getKey, name='getKey'),
]
