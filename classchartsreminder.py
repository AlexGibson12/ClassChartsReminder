import requests
import json
import time
import arrow
import datetime
from plyer import notification
secrets = open("secrets.txt","r").readlines()
CLASSCHARTS_AUTHORIZATION = secrets[0].strip()
CLASSCHARTS_COOKIE = secrets[1].strip()
while True:
    headers = {
    'authorization': CLASSCHARTS_AUTHORIZATION,
    'cookie': CLASSCHARTS_COOKIE
    }
    params = (('date', arrow.now().format('YYYY-MM-DD')),)
    response = requests.get(
        'https://www.classcharts.com/apiv2student/timetable/',
        headers=headers,
        params=params
     ).text
    for lesson in json.loads(response)["data"]:
        now = datetime.datetime.now()
        start = datetime.datetime.strptime(
        lesson["start_time"], '%Y-%m-%dT%H:%M:%S+00:00')
        if now.hour == start.hour and now.minute == start.minute:
            notification.notify( 
            title = "ClassCharts", 
            message=f'You have {lesson["subject_name"]} now', 
            timeout=5) 
    time.sleep(60)
