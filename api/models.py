from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import pytz


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
    """プレイヤー（Userモデルの拡張モデル）"""
    user = models.OneToOneField(User, primary_key=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return "%s, %d pts" % (self.user.username, self.points)


class CorrectSubmit(models.Model):
    """正解の提出ログ"""
    problem = models.ForeignKey(Problem)
    player = models.ForeignKey(Player)
    # データベースに保存するとタイムゾーン設定がUTCに変更される
    # 取り出してからastimezone()を使えばJSTで表示可能
    time = models.DateTimeField(default=now)

    def __str__(self):
        jst = pytz.timezone('Asia/Tokyo')
        return "%s, %s, %s" % (self.problem.name, self.player.user.username, self.time.astimezone(jst))