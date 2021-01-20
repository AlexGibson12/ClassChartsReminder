import requests
import json
import time
import arrow
import datetime
import posixpath
from plyer import notification
classcharts_home_url = "https://www.classcharts.com/"
classcharts_api_url = posixpath.join(classcharts_home_url, "apiv2student")
classcharts_login_url = posixpath.join(classcharts_api_url, "login")
classcharts_timetable_url = posixpath.join(classcharts_api_url, "timetable")
CLASSCHARTS_CODE = "YOURCODEHERE"
CLASSCHARTS_DOB = "DD/MM/YYYY"
while True:
    params = (('date', arrow.now().format('YYYY-MM-DD')),)

    login = requests.post(classcharts_login_url, cookies={
        "cc-session": requests.get(classcharts_home_url).cookies["cc-session"]
    }, data={
        "_method": "POST",
        "code": CLASSCHARTS_CODE,
        "dob": CLASSCHARTS_DOB,
        "remember_me": "true",
        "recaptcha-token": "no-token-available"
    }).json()

    timetable = requests.get(classcharts_timetable_url, headers={
        "Authorization": f'Basic {login["meta"]["session_id"]}'
    }, params=params).json()["data"]

    for lesson in timetable:
        now = datetime.datetime.now()
        start = datetime.datetime.strptime(
            lesson["start_time"], '%Y-%m-%dT%H:%M:%S+00:00')
        if now.hour == start.hour and now.minute == start.minute:
            notification.notify(
                title="ClassCharts",
                message=f'You have {lesson["subject_name"]} now',
                timeout=5)
    time.sleep(60)

