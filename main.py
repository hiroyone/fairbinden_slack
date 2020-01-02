from flask import Flask, render_template, request, redirect, url_for, jsonify
from lunch_fairbinden import main

app = Flask(__name__)

@app.route('/post_to_slack_channel')
def postToSlackChannel():
    import datetime
    weekday=datetime.datetime(2019, 3, 1, 23, 50, 4, 978401, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400), 'JST'))
    response=main(request='',now=weekday, env='PRD')
    return "<span style='font-size:2vw;'>Status {}".format(response)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)


