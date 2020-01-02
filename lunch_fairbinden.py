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

# # Library Import

# Library
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup    
import ssl
from urllib.parse import urljoin
import datetime
import re
import sys
import requests, json
import logging
import os


# +
# Ignore SSL certificate errors 
ctx = ssl.create_default_context() 
ctx.check_hostname= False 
ctx.verify_mode = ssl.CERT_NONE

# Alternative Logger practice: https://realpython.com/python-logging/
# Create and configure logger
LOG_FORMAT = '%(levelname)s - %(asctime)s - %(message)s'


logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()
# -

# # Get today and check weekday

# +
def now_today():
    logger.info("now_today fn")
    # タイムゾーンの生成
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    now =datetime.datetime.now(JST)
    if now.hour < 11:
        now = now - datetime.timedelta(1) # if "now" is before 11am, then take a previous date
    logger.info("now_today is {}".format(now))
    return now

# weekday=datetime.datetime(2019, 2, 26, 23, 50, 4, 978401, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400), 'JST'))
# weekend =datetime.datetime(2019, 3, 2, 23, 50, 4, 978401, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400), 'JST'))
# print(weekday)
# print(weekend)

# +
def check_weekday(now):
    logger.info("check_weekday")
    if now.isoweekday() <= 5:
        return True
    else:
        return False

# weekday_bl=check_weekday(weekday)
# weekend_bl=check_weekday(weekend)
# print(weekday_bl)
# print(weekend_bl)
# -

# # Get daily url

# +
def get_daily_url(now):
    logger.info("get_daily_url fn")
    if (check_weekday(now)):
        logger.info("It is a weekday")
        # It should be weekday
        # Get today's date
        date = '/'.join([str(now.year), now.strftime('%m'), now.strftime('%d') ])
        # Contruct today's url
        domain = 'http://xn--jvrr89ebqs6yg.tokyo/'
        day_url = urljoin(domain, date)
        logger.info("Today's URL is {}".format(day_url))
        #day_url = 'http://xn--jvrr89ebqs6yg.tokyo/2019/02/22' #Stub

        # Find today's menu url
        day_html = urllib.request.urlopen(day_url, context=ctx).read()
        day_soup = BeautifulSoup(day_html, 'html.parser')
        links=day_soup.find_all('a') # Get all link tags
        urls =[link.get('href') for link in links] # Read only url parts
        menu_url = [url for url in urls if url.startswith(day_url)][0] # get a menu url by forward matching
        logger.info("Menu URL is {}".format(menu_url))
        return menu_url
    else:
        logger.info("Menu URL is not returned because it is not a weekday today")
        return
    
# menu_url = get_daily_url(now_today())
# print(get_daily_url(weekday))
# print(get_daily_url(weekend))
# -

# # Get title from the page

# +
def get_title(url):
    logger.info("get_title fn")
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Get texts from the page
    title = soup.select('.post_title')[0]
    logger.info("Title is {}".format(title.text))
    return title.text

# menu_url = 'http://xn--jvrr89ebqs6yg.tokyo/2019/03/01/%e4%b8%8b%e4%bb%81%e7%94%b0%e3%83%9f%e3%83%bc%e3%83%88%e3%81%ae%e5%a1%a9%e9%ba%b9%e6%bc%ac%e3%81%91%e3%82%aa%e3%83%bc%e3%83%96%e3%83%b3%e7%84%bc%e3%81%8d/'
# print(get_title(menu_url))
# -

# # Get main texts from the page

# +
def get_maintexts(url):
    logger.info("get_maintexts fn")
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Get texts from the page
    single_post = soup.select('#single_post')[0]
    texts=single_post.find_all('p')
    clean_texts=[text.text for text in texts]
    print(clean_texts)
    dropna_texts = [text for text in clean_texts if re.match('\w', text)]
    stylized_texts = ['*{}'.format(text) for num,text in enumerate(dropna_texts)] # Add * in the left-hand side
    stylized_texts = [text.replace('\n', '*\n') for text in stylized_texts] # Add * in the right-hand side
    logger.info("Main text is {}".format(stylized_texts))
    return stylized_texts 

# menu_url=get_daily_url(now_today())
# get_maintexts(menu_url)
# print(get_maintexts(menu_url))

# +
def get_mainimage(url):
    logger.info("get_mainimage fn")
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Get images from the page
    single_post = soup.select('#single_post')[0]
    images =single_post.find_all('img')
    image_urls=[image.get('src') for image in images]
    if len(image_urls)==0:
        image_url=""
    else:
        image_url=image_urls[0]
    logger.info("Main image URL is {}".format(image_url))
    return image_url

# Get the last image
# image_url=get_mainimage(menu_url)
# image_url
# print(image_url)

# +
# Create today's date in Japanese
def get_Japanese_date(now): 
    logger.info("get_Japanese_date fn: now is {}".format(now))
    yobi_list = ["月","火","水","木","金","土","日"]
    yobi = yobi_list[now.weekday()]
    date = '{}月{}日({})'.format(now.month,now.day, yobi)
    logger.info("Today's date is {}".format(date))
    return date

# print(get_Japanese_date(weekday))
# -

def main(request, now=now_today(), env="PRD"):
    now=now_today() # 引数のnowの値がなぜか更新されていないっぽいので実験で入れてみる
    logger.info("main fn")
    if env=="PRD":
        # Set up channel urls for productin and staging before cloud function is deployed and triggered        
        WEB_HOOK_URL = os.environ.get('Channel_PRD', 'Environment variable for the production channel is not set.')
    elif env=="STG":
        WEB_HOOK_URL = os.environ.get('Channel_STG', 'Environment variable for the staging channel is not set.')
    else:
        raise ValueError("The value must be either PRD or STG")

    try:
        menu_url = get_daily_url(now)
    except Exception as e: 
        print(e)
        
    if menu_url is None:
        return "It is weekend. No posting to Slack!"
    else:
        post_json = {
            # "channel": "#lab_lunch_fairbinden ",
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": "#36a64f",
                    "pretext": get_Japanese_date(now)+"のランチです！",
                    "author_name": "フェアビンデン",
                    "author_link": "http://xn--jvrr89ebqs6yg.tokyo/",
                    "author_icon": "http://flickr.com/icons/bobby.jpg",
                    "title": get_title(menu_url),
                    "title_link": menu_url,
                    "text": '\n'.join(get_maintexts(menu_url)),
                    "image_url": get_mainimage(menu_url),
                    #"thumb_url": "http://example.com/path/to/thumb.png",
                    "footer": "800円 12:00-14:00",
                    #"footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                    "ts": now.timestamp() # Time Stamp in Unix
                } 
            ]}
        response=requests.post(WEB_HOOK_URL, data = json.dumps(post_json))
        logger.info("Response Status code is {}".format(response.status_code))
    return str(response.status_code)

if __name__ == "__main__":
    logger.info("Run main fn")
    main(request='', now=now_today(), env='STG')
# + {}
# print(main(request='', now=weekday, env='STG'))
# print(main(request='', now=weekend, env='STG'))
# -


