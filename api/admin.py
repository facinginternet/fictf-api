from django.contrib import admin

from api.models import Problem, Player, CorrectSubmit


class ProblemAdmin(admin.ModelAdmin):
    list_filter = ('genre', )
    list_display = ('id', 'name', 'genre', 'points')
    list_display_links = ('id', 'name',)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'points')

    def id(self, player):
        return player.user.id


class CorrectSubmitAdmin(admin.ModelAdmin):
    list_filter = ('player', 'problem', 'time')
    list_display = ('id', 'problem', 'player', 'time')
    list_display_links = ('id', 'problem',)



admin.site.register(Problem, ProblemAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(CorrectSubmit, CorrectSubmitAdmin)