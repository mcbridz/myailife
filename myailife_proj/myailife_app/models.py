from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + "-" + self.date_posted.strftime('%m/%d %I:%M %p')


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='comments')
    text = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.PROTECT, related_name='comments')
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey(
        "self", on_delete=models.PROTECT, related_name='replies', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.post.title + "-" + self.date_posted.strftime('%m/%d %I:%M %p')
