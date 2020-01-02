# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from lunch_fairbinden import *
import datetime
import pytest


# Constant values for test
weekday=datetime.datetime(2019, 3, 1, 23, 50, 4, 978401, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400), 'JST'))
weekend =datetime.datetime(2019, 3, 2, 23, 50, 4, 978401, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400), 'JST'))
menu_url = 'http://xn--jvrr89ebqs6yg.tokyo/2019/03/01/%e4%b8%8b%e4%bb%81%e7%94%b0%e3%83%9f%e3%83%bc%e3%83%88%e3%81%ae%e5%a1%a9%e9%ba%b9%e6%bc%ac%e3%81%91%e3%82%aa%e3%83%bc%e3%83%96%e3%83%b3%e7%84%bc%e3%81%8d/'

def test_check_weekdayl():
    res = check_weekday(weekday)
    assert res==True
def test_check_weekendl():
    res = check_weekday(weekend)
    assert res==False


# +
def test_get_weekday_response():
    res = get_daily_url(weekday)
    res== 'http://xn--jvrr89ebqs6yg.tokyo/2019/03/01/%e4%b8%8b%e4%bb%81%e7%94%b0%e3%83%9f%e3%83%bc%e3%83%88%e3%81%ae%e5%a1%a9%e9%ba%b9%e6%bc%ac%e3%81%91%e3%82%aa%e3%83%bc%e3%83%96%e3%83%b3%e7%84%bc%e3%81%8d/'

def test_get_weekend_response():
    res = get_daily_url(weekend)
    res== None
# -


def test_get_title():
    res = get_title(menu_url)
    assert res== '下仁田ミートの塩麹漬けオーブン焼き'


def test_get_maintexts(): 
    res = get_maintexts(menu_url)
    assert res== ['*群馬県下仁田ミートの豚肉を使って*', '群馬県下仁田ミートの豚バラ肉をビンデン自家製塩麹に漬け込んであります。自家製塩麹のやわらかい風味がついた国産豚肉のおいしさを味わってください。神奈川県三浦のキャベツと船橋農産物供給センターの水菜を50℃洗いにして添えました。', '*切り干し大根の煮物*', '宮崎県綾町の天日干しの切り干し大根に長崎県平戸のアゴちくわと国産大豆１００％使用の油揚げ、奈良県産ニンジンを加えて、丸大豆醤油、本みりん、日本酒、砂糖で煮ました。', '*ガリトマト*', '埼玉県吉田農園のトマトに高知県産生姜で作った酢生姜と丸大豆醤油で味付けしました。箸休めにどうぞ。']


def test_get_mainimage():
    image_url = get_mainimage(menu_url)
    assert image_url=='http://xn--jvrr89ebqs6yg.tokyo/wp-content/uploads/2019/03/A8060FDD-BAD0-4696-B184-54131ADF365E-1024x768.jpeg'    


def test_get_Japanese_date():
    res = get_Japanese_date(weekday)
    assert res== '3月1日(金)'


def test_main_weekday():
    res = main(request='', now=weekday, env="STG")
    assert res== 200
def test_main_weekend():
    res = main(request='', now=weekend, env="STG")
    assert res== 'It is weekend. No posting to Slack!'

if __name__ == '__main__':
    unittest.main()


