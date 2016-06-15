from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from dateutil import tz


class Problem(models.Model):
    """問題"""
    name = models.CharField('問題名', max_length=255, blank=False)
    genre = models.CharField('ジャンル', max_length=127, default="")
    points = models.IntegerField('点数', default=0)
    description = models.TextField('問題文', default="")
    flag = models.CharField('FLAG', max_length=127, default="")

    def __str__(self):
        return self.name


class Player(models.Model):
    """プレイヤー（Userモデルの拡張モデル）"""
    user = models.OneToOneField(User, primary_key=True)
    points = models.IntegerField('獲得点数', default=0)

    def __str__(self):
        return self.user.username


class CorrectSubmit(models.Model):
    """正解の提出ログ"""
    problem = models.ForeignKey(Problem)
    player = models.ForeignKey(Player)
    # データベースに保存するとタイムゾーン設定がUTCに変更される
    # 取り出してからastimezone()を使えばJSTで表示可能
    time = models.DateTimeField('提出時刻', default=now)

    def __str__(self):
        return "%s, %s, %s" % (self.problem.name, self.player.user.username, self.time.astimezone(tz.tzlocal()))