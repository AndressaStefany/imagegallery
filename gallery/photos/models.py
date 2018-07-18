from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    level = models.IntegerField(default=2)
    name = models.CharField(max_length=255)
    date = models.DateTimeField('creation date')


class Photos(models.Model):
    id = models.IntegerField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # photo ImageField
    description = models.CharField(max_length=255)
    date = models.DateTimeField('creation date')
    authorized = models.BooleanField(default=False)
    quantity_like = models.IntegerField(default=0)
