from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Comment, Post


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
