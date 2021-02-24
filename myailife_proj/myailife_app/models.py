from django.db import models


class Post(models.Model):
    text = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.PROTECT, related_name='comments')
    is_reply = models.BooleanField()
    reply = models.ForeignKey(
        "self", on_delete=models.PROTECT, related_name='replies', blank=True, null=True)
