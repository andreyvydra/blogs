from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Blogger(AbstractUser):
    subscriptions = ArrayField(models.IntegerField(), blank=True, null=True)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    headline = models.TextField()
    text = models.TextField()
    create_date = models.DateTimeField()
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    views = ArrayField(models.IntegerField(), blank=True, null=True)
