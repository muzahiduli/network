from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User)
    
    def likesCount(self):
        return self.likes.all().count()

    def likeList(self):
        return self.likes.all()

class Follow(models.Model):
    follower = models.OneToOneField(User, on_delete=models.CASCADE, related_name="follows")
    following = models.ManyToManyField(User)