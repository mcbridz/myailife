from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Comment, Post, SessionObject
import django.contrib.auth
from django.contrib.auth.models import User
from django.utils import timezone
import json
import random
import datetime

# Utility functions


def generate_upper():
    return chr(random.randrange(65, 91))


def generate_lower():
    return chr(random.randrange(97, 123))


def generate_special_char():
    return chr(random.randrange(33, 48))


def generate_num():
    return str(random.randrange(0, 10))


def split(word):
    return [char for char in word]


def generate_session_key():
    key = ''
    for num in range(4):
        key += generate_upper()
        key += generate_lower()
        key += generate_special_char()
        key += generate_num()
    key = split(key)
    shufflingTime = random.randrange(0, 9) + 7
    shufflingTime *= 17
    for i in range(shufflingTime):
        random.shuffle(key)
    return ''.join(key)


def generate_session_object(new_key, new_user):
    print(new_key, new_user)
    new_session_object = SessionObject(
        user_account=None if new_user.is_anonymous else new_user, key=new_key)
    new_session_object.save()
    # This is where we will always delete old objects (>2 days)
    old_session_objects = SessionObject.objects.filter(
        date_created__lte=(timezone.now() - datetime.timedelta(days=2)))
    for obj in old_session_objects:
        obj.delete()


def validate_session_key(key, user):
    session_object = SessionObject.objects.filter(key=key, user=user)
    return session_object.exists()


def check_session_object(key, user):
    return SessionObject.object.filter(user=user, key=key).exists()


def get_key(request):
    key = validate_session_key()
    print(key)
    user = request.user
    generate_session_object(key, user)
    return JsonResponse({'key': key})


def index(request):
    key = validate_session_key()
    user = request.user
    generate_session_object(key, user)
    context = {'key': key}
    return render(request, 'myailife_app/index.html', context)


def get_posts(request):
    posts = Post.objects.all().order_by('date_posted')
    post_list = []
    for post in posts:
        comments_list = []
        comments = Comment.objects.filter(post=post.id, is_reply=False)
        if comments:
            for comment in comments:
                replies = Comment.objects.filter(
                    post=post.id, is_reply=True, reply=comment.id)
                replies_list = []
                if replies:
                    for reply in replies:
                        replies_list.append({
                            'username': comment.user.username if not comment.anonymous else 'Anonymous',
                            'text': comment.text,
                            'date': comment.date_posted.strftime('%m/%d %I:%M %p'),
                            'comment_id': comment.id
                        })
            comments_list.append({
                'username': comment.user.username if not comment.anonymous else 'Anonymous',
                'text': comment.text,
                'date': comment.date_posted.strftime('%m/%d %I:%M %p'),
                'comment_id': comment.id,
                'replies': replies_list,
            })
        post_list.append({
            'title': post.title,
            'text': post.text,
            'date_posted': post.date_posted.strftime('%m/%d %I:%M %p'),
            'id': post.id,
            'comments': comments_list
        })
    return JsonResponse({'posts': post_list})


def add_post(request):
    new_post_data = json.loads(request.body)
    new_post = Post(title=new_post_data['subject'], text=new_post_data['text'])
    new_post.save()
    return JsonResponse({'message': 'Post Added'})


def delete_post(request):
    post_id = json.loads(request.body)['id']
    post = Post.objects.filter(id=post_id)
    if post.exists():
        post.delete()
        return JsonResponse({'message': 'Post Deleted'})
    else:
        return JsonResponse({'message': 'An Error Occurred, Please Contact Administrator Error Type: "Mismatched Post ID"'})


def new_comment(request):
    new_comment_data = json.loads(request.body)


def register(request):
    username = request.POST['username']
    password = request.POST['password']
    vpassword = request.POST['vpassword']
    email_address = request.POST['emailAddress']
    if password != vpassword:
        return JsonResponse({'message': 'passwords do not match, please try again.'})
    else:
        user = User.objects.create_user(username, email_address, password)
        django.contrib.auth.login(request, user)
        return JsonResponse({'message': 'User created and logged in.'})


def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = django.contrib.auth.authenticate(
        request, username=username, password=password)
    message = ''
    if user is not None:
        django.contrib.auth.login(request, user)
        key = validate_session_key()
        generate_session_object(key, user)
        message = 'Logged in successfully.'
    else:
        key = validate_session_key()
        user = request.user
        generate_session_object(key, user)
        message = 'Unable to log in.'
    return JsonResponse({'message': message, 'key': key})


def logout(request):
    django.contrib.auth.logout(request)
    return JsonResponse({'message': 'Log out successful.'})
