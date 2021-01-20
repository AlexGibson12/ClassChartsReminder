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
    subjects = [(
        datetime.datetime.strptime(i["start_time"], '%Y-%m-%dT%H:%M:%S+00:00'),
        i["subject_name"])
        for i in json.loads(response)["data"]]

    for i in subjects:
        now = datetime.datetime.now()
        if now.hour == i[0].hour and now.minute == i[0].minute:
            notification.notify( 
            title = "ClassCharts", 
            message=f'You have {i[1]} now', 
            timeout=5) 
    time.sleep(60)
