# coding:utf-8
from importlib import reload
import sys
reload(sys)
import requests
from flask import render_template, redirect, flash, \
    url_for, request, current_app, jsonify
from . import api

@api.route('/tasks', methods=['GET'])
def get_tasks():
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
        print(weather_dict)
        return str(weather_dict)

    except Exception as exception:
        print(exception)
        return {}