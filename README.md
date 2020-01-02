# Lunch Notification Bot for Fairbinden

This program is to scrape daily lunch menu at Fairbinden blog and extract the main information to send to your Slack channel during weekdays.

Tech Stack
- Python
- Flask
- BeautifulSoup
- CloudFunction
- App Engine
- Cloud Scheduler

1. Set up channel urls for productin and staging as export variables before cloud function is deployed and triggered        

Examples
```
export Channel_PRD = "https://hooks.slack.com/services/xxxxxx/xxxxx/xxxxxxxxxxxxxxxxxxxxx"
export Channel_STG = "https://hooks.slack.com/services/qqqqqq/sssss/sssssssssssssssssssss"
```

2. Deploy the code to Cloud Function with Python3 runtime

3. Set up a cloud scheduler to trigger the function at 10 a.m. every Weekday 

* You can also use main.py to launch the same program through App Engine, just for fun. Linux&Python docker image is also attached to this file.