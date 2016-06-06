from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    """問題"""
    name = models.CharField('問題名', max_length=255)
    
    def __str__(self):
        return self.name


class Player(models.Model):
    """プレイヤー"""
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username
