from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^problems_list$', views.problems_list, name='problems_list'),
    url(r'^problem/(?P<prob_id>(\d+))$', views.problem, name='get_problem'),
]
