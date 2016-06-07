from django.http import HttpResponse
from django.shortcuts import render
from api.models import *
import json

def problems_list(request):
    """api/problems_list
    全てのProblemをjson形式で送り返す"""
    problems_dict = {}
    for prob in Problem.objects.all():
        problems_dict[prob.id] = {'name': prob.name, 'category': prob.category, 'points': prob.points}
    return HttpResponse(json.dumps(problems_dict))

def get_problem(request, prob_id):
    """api/get_problem/(id)
    idのProblemをjson形式で送り返す"""
    problem = Problem.objects.get(id=prob_id)
    problem_dict = {'name': problem.name, 'category': problem.category, 'points': problem.points, "description": problem.description}
    return HttpResponse(json.dumps(problem_dict))