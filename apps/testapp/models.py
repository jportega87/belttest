from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Login(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    login = models.ManyToManyField(Login)
