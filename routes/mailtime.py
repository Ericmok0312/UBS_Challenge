import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def solve(emails, ans):
    record = {}
    for email in emails:
        subject = email["subject"]
        subject_order = subject.split(": ")[-1] + str(len(subject.split(": ")))
        sender = email["sender"]
        receiver = email["receiver"]
        time = email["timeSent"] 
        timeSplit = {}
        date_time = time.split('T')
        time_part = date_time[1].split('+')[0]
        timeSplit['year'] = int(date_time[0][:4])
        timeSplit['month'] = int(date_time[0][5:7])
        timeSplit['day'] = int(date_time[0][8:])
        timeSplit['hour'] = int(time_part[:2])
        timeSplit['minute'] = int(time_part[2:4])
        timeSplit['second'] = int(time_part[4:])
        if time_part[8] == '+':
            timeSplit['timezone'] = int(time_part[9:11])
        else:
            timeSplit['timezone'] = int(time_part[9:11]) * -1

        if not record[sender]:
            record[sender] = {}
        if not record[receiver]:
            record[receiver] = {}
        if not subject[0:3] == "Re:":
            record[sender][subject_order] = timeSplit
        record[receiver][subject_order] = timeSplit
    for user, emails in record.items():
        total_time = 0
        emails = sorted(emails, key=lambda x: next(iter(x)))
        times = emails.value()
        for i in range(len(times))[0::2]:
            if i+1 == len(times):
                break
            year = times[i+1]["year"] - times[i]["year"]
            month = times[i+1]["month"] - times[i]["month"]
            day = times[i+1]["day"] - times[i]["day"]
            hour = (times[i+1]["hour"] - time[i+1]['timezone']) - (times[i]["hour"] - times[i]['timezone'])
            minute = times[i+1]["minute"] - times[i]["minute"]
            second = time[i+1]["second"] - times[i]["second"]
            total_time = (year * 12 + month) + day + hour + minute + second + 
            
        ans[user] = 
        



@app.route('/digital-colony', methods=['POST'])
def digital_colony():
    data = request.get_json()
    emails = data["emails"]
    ans = {}
    solve(emails, ans)
    return json.dumps(ans)