from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=600, null=True)
    likes = models.IntegerField(default=0)
    already_liked = models.ManyToManyField(User, related_name='already_liked')
    already_disliked = models.ManyToManyField(User, related_name='already_disliked')
    dislikes = models.IntegerField(default=0)
    no_of_comment = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
        
    def get_like_count(self):
        return self.likes
    
    def liked_by(self, user):
        return self.already_liked.filter(id=user.id).exists()

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
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.username

class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.post.title
