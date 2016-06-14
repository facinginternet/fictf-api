from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^problems_list/$', views.problems_list, name='problems_list'),
    url(r'^problem/(?P<problem_id>(\d+))/$', views.problem, name='problem'),
    url(r'^players_list/$', views.players_list, name='players_list'),
    url(r'^player/(?P<player_id>(\d+))/$', views.player, name='player'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^solved_problems/(?P<player_id>(\d+))/$', views.solved_problems, name='solved_problems'),
    url(r'^login_player/$', views.login_player, name='login_player'),
    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^login_test/$', views.login_test),
    url(r'^signup_test/$', views.signup_test),
    url(r'^submit_test/$', views.submit_test),
]
