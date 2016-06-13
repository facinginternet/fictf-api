from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    """問題"""
    name = models.CharField('問題名', max_length=255, blank=False)
    category = models.CharField('カテゴリ名', max_length=127, default="")
    points = models.IntegerField(default=0)
    description = models.CharField('問題文', max_length=8191, default="")
    flag = models.CharField('カテゴリ名', max_length=127, default="")

    def __str__(self):
        return self.name


class Player(models.Model):
    """プレイヤー"""
    user = models.OneToOneField(User)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class CorrectSubmit(models.Model):
    """正解の提出"""
    problem = models.ForeignKey(Problem)
    player = models.ForeignKey(Player)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s, %s, %s" % (self.problem.name, self.player.name, self.time)