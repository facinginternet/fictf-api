from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^problems_list$', views.problems_list, name='problems_list'),
    url(r'^problem/(?P<problem_id>(\d+))$', views.problem, name='problem'),
    url(r'^players_list$', views.players_list, name='players_list'),
    url(r'^player/(?P<player_id>(\d+))$', views.player, name='player'),
    url(r'^solved_problems/(?P<player_id>(\d+))$', views.solved_problems, name='solved_problems'),
]
