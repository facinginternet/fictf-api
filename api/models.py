from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    """問題"""
    name = models.CharField('問題名', max_length=255, blank=False)
    genre = models.CharField('カテゴリ名', max_length=127, default="")
    points = models.IntegerField(default=0)
    description = models.CharField('問題文', max_length=8191, default="")
    flag = models.CharField('カテゴリ名', max_length=127, default="")

    def __str__(self):
        return "%s, [%s], %d pts" % (self.name, self.genre, self.points)


class Player(models.Model):
    """プレイヤー（Userモデルの拡張）"""
    user = models.OneToOneField(User, primary_key=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return "%s, %d pts" % (self.user.username, self.points)


class CorrectSubmit(models.Model):
    """正解の提出ログ"""
    problem = models.ForeignKey(Problem)
    player = models.ForeignKey(Player)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s, %s, %s" % (self.problem.name, self.player.user.username, self.time)