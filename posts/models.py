from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=600, null=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_by')
    disliked_by = models.ManyToManyField(User, related_name='disliked_by')
    dislikes = models.IntegerField(default=0)
    saved_by = models.ManyToManyField(User, related_name='saved_by')
    no_of_comment = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
        
    def get_like_count(self):
        return self.likes

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    posts = models.ManyToManyField(Post, related_name='your_posts')
    
    def __str__(self):
        return self.user.username
