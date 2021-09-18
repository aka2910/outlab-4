from django.db import models


# Create your models here.

class Profile(models.Model):
    username = models.CharField(max_length=150, primary_key=True, default=None)
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=30, null=True)
    avatar_url = models.CharField(max_length=100, null=True)
    follower_count = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)


class Repository(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=100, null=True)
    repo_stars = models.IntegerField()
