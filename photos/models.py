from django.db import models
from django.contrib.auth.models import User
import datetime


def user_directory_path(instance, filename):
    # file will be uploaded to _ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    # image = models.ImageField(upload_to=user_directory_path)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    authorized = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    def __str__(self):
        return '{}_{}'.format(self.path,self.description)

class LikeTable(models.Model):
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)