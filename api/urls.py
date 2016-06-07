from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^problems_list$', problems_list, name='problems_list'),
    url(r'^get_problem/(\d+)', get_problem, name='get_problem'),
    # url(r'^get_problem/(?P<prob_id>(\d+))$', get_problem, name='get_problem'),
]
