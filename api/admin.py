from django.contrib import admin
from django.contrib.auth.models import Permission
from api.models import Problem, Player, CorrectSubmit
from django.contrib.contenttypes.models import ContentType


class ProblemAdmin(admin.ModelAdmin):
    list_filter = ('genre', 'author', )
    list_display = ('id', 'name', 'genre', 'points', 'author', )
    list_display_links = ('id', 'name',)
    fieldsets = (
        (None, {'fields': ('name', 'genre', 'points', 'description', 'flag',)}),
    )

    def get_queryset(self, request):
        # 自分が author である problem のみ表示
        qs = super(ProblemAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            player = request.user.player
            return qs.filter(author=player)
        except Player.DoesNotExist:
            return qs.none()

    def get_fieldsets(self, request, obj=None):
        # 管理者のみ author の変更を可能にする
        fieldsets = super(ProblemAdmin, self).get_fieldsets(request, obj)
        if request.user.is_superuser:
            return fieldsets + (('管理者のみ', {'fields': ('author',)}),)
        return fieldsets

    def save_model(self, request, problem, form, change):
        # author を編集した player に設定する
        if not request.user.is_superuser:
            problem.author = request.user.player

        super(ProblemAdmin, self).save_model(request, problem, form, change)
        if 'points' in form.changed_data:
            # 点数に変更があった場合，この problem を解いたことがある全ての player の獲得点数を再計算する
            recalculate_points(problem)


def recalculate_points(problem):
    """引数の problem を解いたことがある全ての player の獲得点数を再計算する"""
    for prob_submit in problem.submits.all():
        player = prob_submit.player
        points = 0
        for plyr_submit in player.submits.all():
            solved_prob = plyr_submit.problem
            points += solved_prob.points
        player.points = points
        player.save()


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'points')
    fieldsets = (
        (None, {'fields': ('user', 'points', )}),
    )
    readonly_fields = ('points', )

    def id(self, player):
        return player.user.id

    def get_actions(self, request):
        # 管理者のみ grant_problems_edit_permission を呼び出せるようにする
        actions = super(PlayerAdmin, self).get_actions(request)
        if request.user.is_superuser:
            gpep = PlayerAdmin.grant_problems_edit_permission
            actions['grant_problems_edit_permission'] = (gpep, 'grant_problems_edit_permission', gpep.short_description)
            return actions
        else:
            return actions

    def grant_problems_edit_permission(self, request, players):
        # 選択された player に problems を編集する権限を与える
        for player in players:
            user = player.user
            user.is_staff = True
            prob_ct = ContentType.objects.get_for_model(Problem)
            permissions = Permission.objects.filter(content_type=prob_ct)
            for permission in permissions:
                user.user_permissions.add(permission)
            user.save()
    grant_problems_edit_permission.short_description = "選択された players に problems を編集する権限を与える"


class CorrectSubmitAdmin(admin.ModelAdmin):
    list_filter = ('player', 'problem', 'date')
    list_display = ('id', 'problem', 'player', 'date')
    list_display_links = ('id', 'problem',)


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(CorrectSubmit, CorrectSubmitAdmin)