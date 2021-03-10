from django.urls import path
from . import views

app_name = 'myailife'

urlpatterns = [
    path('', views.index, name='index'),
    path('getPosts', views.getPosts, name='getPosts'),
    path('addPost', views.addPost, name='addPost'),
    path('deletePost', views.deletePost, name='deletePost'),
    path('register', views.register, name='register'),
    path('getKey', views.getKey, name='getKey'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
