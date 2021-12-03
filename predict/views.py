from bson import ObjectId
from django.shortcuts import render, get_object_or_404, redirect
import datetime
from django.utils.dateformat import DateFormat
from pymongo import MongoClient
from home.models import *
from predict.models import *
from logic.predict import *
# Create your views here.
def match_list(request) :
    today = DateFormat(datetime.datetime.now()).format('Ymd')
    date = request.GET.get('dates')
    game = request.GET.get('game')

    if date is None or date == '' :
        # 시작일 지정
        date_conver = "20211005"
    else :
        date_conver = date.replace("-", "")
    matches = Matches.objects.filter(date=date_conver).order_by('id')

    if game is not None:
        game_info = findMatch(game)
        away = game_info['away']
        home = game_info['home']
        period = request.GET.get('period')
    else:
        game_info = matches[0]
        away = game_info.away
        home = game_info.home
        period = request.GET.get('period')
        if period is None:
            period = "1"

    article_upper = article_based(away, home, period, date_conver)
    stat_upper = stat_based(away, home, date_conver)

    context = {
        'matches': matches,
        'game_info': game_info,
        'period': period,
        'date': date,
        'article_upper': article_upper,
        'stat_upper': stat_upper,
        # 'both_upper': both_upper,
    }

    return render(request, 'predict/predict.html', context)

def findMatch(match_id):
    mongo=MongoClient("mongodb://windup_dba:lotsamhwa@114.129.200.203:28018")
    db=mongo['windup']
    col=db['matches']
    return col.find_one({'_id':ObjectId(match_id)})