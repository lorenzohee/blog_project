# coding:utf-8
from importlib import reload
import sys
import json
reload(sys)
from datetime import datetime
import requests
from flask import render_template, redirect, flash, \
    url_for, request, current_app, jsonify
from . import api

from ..models import Task, Article, ArticleType, article_types, Comment, \
    Follow, User, Source, BlogView
from .forms import TaskSubmitForm, TaskCommonForm
from .. import db, csrf

@api.route('/tasks/weather', methods=['GET'])
def get_weather():
    city_code = "101120201"
    weather_url = 'http://t.weather.sojson.com/api/weather/city/{}'.format(city_code)
    try:
        resp = requests.get(url=weather_url)
        weather_dict = resp.json()
        # 今日天气
        # {
        # "sunrise": "04:45",
        # "high": "高温 34.0℃",
        # "low": "低温 25.0℃",
        # "sunset": "19:37",
        # "aqi": 145,
        # "ymd": "2019-06-12",
        # "week": "星期三",
        # "fx": "西南风",
        # "fl": "3-4级",
        # "type": "多云",
        # "notice": "阴晴之间，谨防紫外线侵扰"
        # }
        today_weather = weather_dict.get('data').get('forecast')[0]
        display = ['ymd', 'week', 'type', 'fx', 'fl', 'high', 'low', 'notice']
        weather_info = ' '.join(today_weather[p] for p in display if today_weather.get(p, None))
        return json.dumps(weather_dict)

    except Exception as exception:
        print(exception)
        return {}

@csrf.exempt
@api.route('/tasks', methods=['GET', 'POST'])
def getTasks():
    if request.method == 'POST':
        data = request.get_data()
        form = TaskCommonForm(request.form)
        if form.validate():
            alert_time = request.json.get('alert_time')
            if alert_time:
                task = Task(title=request.json.get('title'),
                    content = request.json.get('content'),
                    alert_time = datetime.strptime(alert_time, "%Y-%m-%d %H:%M:%S"))
            else:
                task = Task(title=request.json.get('title'),
                    content = request.json.get('content'))
            db.session.add(task)
            db.session.commit()
            return jsonify(task.serialize)
        if form.errors:
            return jsonify({"code": form.errors})
    else:
        page = request.args.get('page', 1, type=int)
        pagination = Task.query.order_by(Task.create_time.desc()).paginate(
                page, per_page=current_app.config['ARTICLES_PER_PAGE'],
                error_out=False)
        tasks = pagination.items
        return jsonify([i.serialize for i in tasks])

@csrf.exempt
@api.route('/tasks/<int:id>', methods=['GET', 'PUT'])
def taskDetailById(id):
    task = Task.query.get_or_404(id)
    if request.method == 'PUT':
        task.title = request.json.get('title')
        task.content = request.json.get('content')
        alert_time = request.json.get('alert_time')
        if alert_time:
            task.alert_time = datetime.strptime(alert_time, "%Y-%m-%d %H:%M:%S")
        if request.json.get('is_finished'):
            task.is_finished = request.json.get('is_finished')
        db.session.add(task)
        db.session.commit()
        return jsonify(task.serialize)
    else:
        return jsonify(task.serialize)

@csrf.exempt
@api.route('/tasks_delete/<int:id>', methods=['DELETE'])
def delTaskById(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return {"code": "error", "message": u'删除失败！'}
    else:
        return {"code": "success", "message": u'删除成功！'}