from django.urls import path
from . import views

app_name = 'myailife'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_posts', views.get_posts, name='getPosts'),
    path('add_post', views.add_post, name='addPost'),
    path('delete_post', views.delete_post, name='deletePost'),
    path('register', views.register, name='register'),
    path('get_key', views.get_key, name='getKey'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
