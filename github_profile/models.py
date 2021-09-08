from django.db import models


# Create your models here.


class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, primary_key=True, default=None)
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=30, null=True)
    follower_count = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)
    last_update.editable = True
    repos = models.JSONField()
