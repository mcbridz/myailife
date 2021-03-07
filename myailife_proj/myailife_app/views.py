from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Comment, Post, SessionObject
from django.utils import timezone
import json
import random
import datetime


def generateUpper():
    return chr(random.randrange(65, 91))


def generateLower():
    return chr(random.randrange(97, 123))


def generateSpChr():
    return chr(random.randrange(33, 48))


def generateNum():
    return str(random.randrange(0, 10))


def split(word):
    return [char for char in word]


def generateSessionKey():
    key = ''
    for num in range(4):
        key += generateUpper()
        key += generateLower()
        key += generateSpChr()
        key += generateNum()
    key = split(key)
    shufflingTime = random.randrange(0, 9) + 7
    shufflingTime *= 17
    for i in range(shufflingTime):
        random.shuffle(key)
    return ''.join(key)


def generateSessionObject(key, user):
    new_session_object = SessionObject(user=user, key=key)
    new_session_object.save()
    # This is where we will always delete old objects (>2 days)
    old_session_objects = SessionObject.objects.filter(
        date_created__lte=(timezone.now() - datetime.timedelta(days=2)))
    for obj in old_session_objects:
        obj.delete()


def checkSessionObject(key, user):
    return SessionObject.object.filter(user=user, key=key).exists()


def index(request):
    context = {}
    return render(request, 'myailife_app/index.html', context)


def getPosts(request):
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


def addPost(request):
    new_post_data = json.loads(request.body)
    new_post = Post(title=new_post_data['subject'], text=new_post_data['text'])
    new_post.save()
    return JsonResponse({'message': 'Post Added'})


def deletePost(request):
    post_id = json.loads(request.body)['id']
    post = Post.objects.filter(id=post_id)
    if post.exists():
        post.delete()
        return JsonResponse({'message': 'Post Deleted'})
    else:
        return JsonResponse({'message': 'An Error Occurred, Please Contact Administrator Error Type: "Mismatched Post ID"'})


def newComment(request):
    new_comment_data = json.loads(request.body)


def getKey(request):
    key = generateSessionKey()
    generateSessionObject(key, request.user)
    return JsonResponse({'key': key})
