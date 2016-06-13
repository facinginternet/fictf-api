from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.models import User
from api.models import Problem, Player, CorrectSubmit
import json


# Todo
# ・CRUDを実装するとき，問題点数が変更された場合は全Playerのpointsを更新するようにする


def problems_list(request):
    """/api/problems_list
    全てのProblemをjson形式で取得する"""
    prob_list = []
    for prob in Problem.objects.all():
        prob_list.append({'problem_id': prob.id, 'name': prob.name, 'category': prob.category, 'points': prob.points})
    problems_json = json.dumps(prob_list, ensure_ascii=False)
    return HttpResponse(problems_json, content_type='application/json')


def problem(request, problem_id):
    """/api/problem/(problem_id)
    引数prob_idのProblemをjson形式で取得する"""
    try:
        problem = Problem.objects.get(id=problem_id)
        problem_dict = {'name': problem.name, 'category': problem.category, 'points': problem.points, "description": problem.description}
        problem_json = json.dumps(problem_dict, ensure_ascii=False)
    except Problem.DoesNotExist:
        # prob_idのProblemが存在しない場合は404を返す
        return HttpResponseNotFound(content_type='application/json')
    return HttpResponse(problem_json, content_type='application/json')


def solved_problems(request, player_id):
    """/api/solved_problems/(player_id)
    player_idのプレイヤーが解いた問題一覧をjson形式で取得する"""
    try:
        player = Player.objects.get(id=player_id)
        submits_list = []
        for sbmt in CorrectSubmit.objects.filter(player=player):
            submits_list.append({'problem_id': sbmt.problem.id, 'time': str(sbmt.time)})
        submits_json = json.dumps(submits_list, ensure_ascii=False)
    except Player.DoesNotExist:
        # player_idのplayerが存在しない場合は404を返す
        return HttpResponseNotFound(content_type='application/json')
    return HttpResponse(submits_json, content_type='application/json')


# Todo
def submit(request):
    """/api/submit
    submitが正しいかどうかを判定し，データベースを操作する"""
    pass


# Todo 引数の実装
def players_list(request):
    """/api/players_list
    引数に基づいてPlayer一覧をjson形式で取得する"""
    players_dict = {}
    for player in Player.objects.all():
        players_dict[player.id] = {'user': player.user.username, 'points': player.points}
    players_json = json.dumps(players_dict, ensure_ascii=False)
    return HttpResponse(players_json, content_type='application/json')


def player(request, player_id):
    """/api/player/(player_id)
    player_idのPlayerをjson形式で取得する"""
    try:
        player = Player.objects.get(id=player_id)
        player_dict = {'user': player.user.username, 'points': player.points}
        player_json = json.dumps(player_dict, ensure_ascii=False)
    except Player.DoesNotExist:
        # player_nameのPlayerが存在しない場合は404を返す
        return HttpResponseNotFound(content_type='application/json')
    return HttpResponse(player_json, content_type='application/json')


# Todo
def login_user(request):
    """/api/login_user
    今ログイン状態ならば，そのユーザの詳細情報をjson形式で取得する"""
    pass