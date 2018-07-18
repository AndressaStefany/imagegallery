from django.db import models


class User(models.Model):
    level = models.IntegerField(default=2)
    name = models.CharField(max_length=255)
    login = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    date = models.DateTimeField()
    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    # file will be uploaded to _ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.CharField(max_length=255)
    date = models.DateTimeField()
    authorized = models.BooleanField(default=False)
    quantity_like = models.IntegerField(default=0)
    def __str__(self):
        return self.description
