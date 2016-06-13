from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from api.models import Problem
import json


def problems_list(request):
    """/api/problems_list
    全てのProblemをjson形式で送り返す"""
    problems_dict = {}
    for prob in Problem.objects.all():
        problems_dict[prob.id] = {'name': prob.name, 'category': prob.category, 'points': prob.points}
    problems_json = json.dumps(problems_dict, ensure_ascii=False)
    return HttpResponse(problems_json, content_type='application/json')


def problem(request, prob_id):
    """/api/problem/(prob_id)
    引数prob_idのProblemをjson形式で送り返す"""
    try:
        problem = Problem.objects.get(id=prob_id)
        problem_dict = {'name': problem.name, 'category': problem.category, 'points': problem.points, "description": problem.description}
        problem_json = json.dumps(problem_dict, ensure_ascii=False)
    except Problem.DoesNotExist:
        # prob_idのProblemが存在しない場合は404を返す
        return HttpResponseNotFound(content_type='application/json')
    return HttpResponse(problem_json, content_type='application/json')


