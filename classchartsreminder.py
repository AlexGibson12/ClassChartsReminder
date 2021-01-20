import requests
import json
import time
import arrow
import datetime
import posixpath
import sys
import subprocess
import os
from plyer import notification

classcharts_home_url = "https://www.classcharts.com/"
classcharts_api_url = posixpath.join(classcharts_home_url, "apiv2student")
classcharts_login_url = posixpath.join(classcharts_api_url, "login")
classcharts_timetable_url = posixpath.join(classcharts_api_url, "timetable")
def notify(code,dob):
    while True:
        params = (('date', arrow.now().format('YYYY-MM-DD')),)
        
        login = requests.post(classcharts_login_url, data = {
            "_method": "POST",
            "code": code,
            "dob": dob,
            "remember_me": "true",
            "recaptcha-token": "no-token-available"
        }).json()

        timetable = requests.get(classcharts_timetable_url, headers = {
            "Authorization": f'Basic {login["meta"]["session_id"]}'
        },params=params).json()["data"]
        print(timetable)
        for lesson in timetable:
            now = datetime.datetime.now()
            start = datetime.datetime.strptime(
            lesson["start_time"], '%Y-%m-%dT%H:%M:%S+00:00')
            if now.hour == start.hour and now.minute == start.minute:
                notification.notify( 
                title = "ClassCharts Reminder",
                app_icon = os.path.abspath("classcharts.ico"),
                message=f'You have {lesson["subject_name"]} now.', 
                timeout=5) 
        time.sleep(60)
if len(sys.argv)<4:
    notify(sys.argv[1],sys.argv[2])
else:
    print("Usage: python3 classchartsreminder.py <yourcode> <dd/mm/yyyy>")

      
