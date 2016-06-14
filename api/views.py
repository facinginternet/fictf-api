from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render
from api.models import Problem, Player, CorrectSubmit
from dateutil import tz
import json


# Todo
# ・CRUDを実装するとき，問題点数が変更された場合は全Playerのpointsを更新するようにする


def problems_list(request):
    """/api/problems_list/
    全てのProblemをjson形式で取得する"""
    prob_list = []
    for prob in Problem.objects.all():
        prob_list.append({'id': prob.id, 'name': prob.name, 'genre': prob.genre, 'points': prob.points})
    problems_json = json.dumps(prob_list, ensure_ascii=False)
    return HttpResponse(problems_json, content_type='application/json')


def problem(request, problem_id):
    """/api/problem/(problem_id)/
    引数prob_idのProblemをjson形式で取得する"""
    try:
        prob = Problem.objects.get(id=problem_id)
        problem_dict = {'name': prob.name, 'genre': prob.genre, 'points': prob.points, "description": prob.description}
        problem_json = json.dumps(problem_dict, ensure_ascii=False)
    except Problem.DoesNotExist:
        # prob_idのProblemが存在しない場合は404を返す
        return HttpResponseNotFound(content_type='application/json')
    return HttpResponse(problem_json, content_type='application/json')


def solved_problems(request, player_id):
    """/api/solved_problems/(player_id)/
    player_idのプレイヤーが解いた問題一覧をjson形式で取得する"""
    try:
        plyr = Player.objects.get(user=player_id)
        submits_list = []
        jst = pytz.timezone('Asia/Tokyo')
        for sbmt in CorrectSubmit.objects.filter(player=plyr):
            submits_list.append({'problem_id': sbmt.problem.id, 'time': str(sbmt.time.astimezone(tz.tzlocal()))})
        submits_json = json.dumps(submits_list, ensure_ascii=False)
    except Player.DoesNotExist:
        # player_idのplayerが存在しない場合は404を返す
        return HttpResponseNotFound(content_type='application/json')
    return HttpResponse(submits_json, content_type='application/json')


@require_POST
def submit(request):
    """[POST] /api/submit/
    POSTで受け取ったflagが正しいかどうかを判定し，成否をjson形式で取得する
    プレイヤーがその問題を解いたのが初めてであった場合，CorrectSubmitレコードを発行する"""
    correct = False
    try:
        problem_id = int(request.POST['problem_id'])
        prob = Problem.objects.get(id=problem_id)
        if request.POST['flag'] == prob.flag:
            correct = True
    except Problem.DoesNotExist or MultiValueDictKeyError or ValueError:
        # prob_idのProblemが存在しない場合，またはPOSTに'flag'が存在しない場合は404を返す
        return HttpResponseNotFound(content_type='application/json')

    if request.user.is_authenticated():
        # ログイン時
        solved = CorrectSubmit.objects.filter(problem=prob, player=request.user.id).count() > 0
        result_json = json.dumps({'correct': correct, 'solved': solved})
        if correct and not solved:
            # プレイヤーが初めてこの問題を正解した
            CorrectSubmit.objects.create(problem=prob, player=Player.objects.get(user=request.user))
            plyr = Player.objects.get(user=request.user)
            plyr.points += prob.points
            plyr.save()
    else:
        # 非ログイン時
        result_json = json.dumps({'correct': correct, 'solved': False})
    return HttpResponse(result_json, content_type='application/json')


def players_list(request):
    """/api/players_list/?(sort, order, num)
    引数に基づいてPlayer一覧をjson形式で取得する"""

    # どのカラムの情報でソートするか（デフォルト: user.id）
    sort_option = 'user'
    if 'sort' in request.GET:
        sort_key = request.GET['sort']
        if sort_key == 'username':
            sort_option = 'user__username'
        elif sort_key == 'points':
            sort_option = 'points'

    # 昇順 or 降順（デフォルト: 昇順）
    sort_reverse_option = ''
    if 'order' in request.GET:
        sort_order = request.GET['order']
        if sort_order == 'desc' or sort_order == 'descension':
            sort_reverse_option = '-'

    # オブジェクトをソートする
    player_objects = Player.objects.all().order_by(sort_reverse_option + sort_option)

    # 取得する件数（デフォルト: 全件）
    num = len(player_objects)
    if 'num' in request.GET and request.GET['num'].isdigit():
        num = min(num, int(request.GET['num']))

    p_list = []
    for i in range(num):
        plyr = player_objects[i]
        p_list.append({'id': plyr.user.id, 'username': plyr.user.username, 'points': plyr.points})

    players_json = json.dumps(p_list, ensure_ascii=False)
    return HttpResponse(players_json, content_type='application/json')


def player(request, player_id):
    """/api/player/(player_id)/
    player_idのPlayerをjson形式で取得する"""
    try:
        plyr = Player.objects.get(user=player_id)
        player_dict = {'username': plyr.user.username, 'points': plyr.points}
        player_json = json.dumps(player_dict, ensure_ascii=False)
    except Player.DoesNotExist:
        # player_nameのPlayerが存在しない場合は404を返す
        return HttpResponseNotFound(content_type='application/json')
    return HttpResponse(player_json, content_type='application/json')


def login_player(request):
    """/api/login_player/
    プレイヤーがログインしている状態ならば，そのプレイヤーの詳細情報をjson形式で取得する"""
    if request.user.is_authenticated():
        plyr = Player.objects.get(user=request.user)
        player_dict = {'username': plyr.user.username, 'email': plyr.user.email, 'points': plyr.points}
        player_json = json.dumps(player_dict, ensure_ascii=False)
    else:
        # ログインしていない場合は404を返す
        return HttpResponseNotFound(content_type='application/json')
    return HttpResponse(player_json, content_type='application/json')


@require_POST
def log_in(request):
    """[POST] /api/login/
    POSTでusernameとpasswordを受け取り，認証を行う．ログイン成否をjson形式で取得する"""
    accept = False
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        auth_user = authenticate(username=username, password=password)
        if auth_user and auth_user.is_active:
            login(request, auth_user)
            accept = True
    result_json = json.dumps({'accept': accept})
    return HttpResponse(result_json, content_type='application/json')


def log_out(request):
    """/api/login/
    ログアウトする．ログアウト成否をjson形式で取得する"""
    logout(request)
    result_json = json.dumps({'accept': True})
    return HttpResponse(result_json, content_type='application/json')


@require_POST
def sign_up(request):
    """[post] /api/signup
    POSTでusernameとpasswordを受け取り，プレイヤーを新規作成する．
    作成に成功した場合はログインする．作成の成否をjson形式で取得する"""
    accept = True
    error = []
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if password == '':
            # passwordが空の場合，作成失敗
            accept = False
            error.append('empty_password')
        elif len(password) < 6:
            # passwordの長さが6文字未満の場合，作成失敗
            accept = False
            error.append('too_short_password')
        if username == '':
            # usernameが空の場合，作成失敗
            accept = False
            error.append('empty_username')
        if accept:
            try:
                user = User.objects.create_user(username=username, password=password)
                Player.objects.create(user=user)
                auth_user = authenticate(username=username, password=password)
                login(request, auth_user)
            except IntegrityError:
                # ユーザ名が重複している場合，作成失敗
                accept = False
                error.append('duplicate_username')
    else:
        accept = False
        error.append('insufficient_POST_data')
    result_json = json.dumps({'accept': accept, 'error': error})
    return HttpResponse(result_json, content_type='application/json')


def login_test(request):
    return render(request, 'login_test.html')


def signup_test(request):
    return render(request, 'signup_test.html')


def submit_test(request):
    return render(request, 'submit_test.html')