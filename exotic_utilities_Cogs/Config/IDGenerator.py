import random
import pyrebase
from datetime import datetime, timedelta
CONFIG = {
    "apiKey": "AIzaSyCWWkICrN3i3PM0Mg9EboKUtpzZRGfMXcA",
    "databaseURL": "https://exotic-utilities-default-rtdb.firebaseio.com",
    "authDomain": "exotic-utilities.firebaseapp.com",
    "projectId": "exotic-utilities",
    "storageBucket": "exotic-utilities.appspot.com",
    "messagingSenderId": "147423121319",
    "appId": "1:147423121319:web:85e506c2b53cefb563b082"
}
firebase = pyrebase.initialize_app(CONFIG)
db = firebase.database()
def IDGenerator(reason):

    alphaList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
         '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "_", "-", "&", "^"]
    previousIDS = db.child("IDs").get().val()
    ID = ""
    previousIDSList = []
    if previousIDS is not None:
        for key, value in previousIDS.items():
            previousIDSList.append(key)
    if reason == "punish":
        flag = True

        while flag:

            for i in range(19):
                ID += random.choice(alphaList)
            if ID in previousIDSList:
                ID = ""
                continue
            else:
                flag = False

    elif reason == "modmail":
        flag = True

        while flag:

            for i in range(19):
                ID += random.choice(alphaList)
            if ID in previousIDSList:
                ID = ""
                continue
            else:
                flag = False

    elif reason == "nickname":
        flag = True

        while flag:

            for i in range(6):
                ID += random.choice(alphaList)
            if ID in previousIDSList:
                ID = ""
                continue
            else:
                flag = False
    print(ID)
    db.child("IDs").update({ID: ID})
    return ID

def modmailCoolDown(message):
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    total_time = 0
    coolDown = "1m"
    tim = coolDown.split()

    ti = [int(''.join(i for i in t if i.isdigit())) for t in tim]

    tl = [(''.join(i for i in t if i.isdigit() == False)) for t in tim]

    for t in range(0, len(tl)):
        total_time += ti[t] * int(time_convert[tl[t]])

    tomorrow = datetime.utcnow() + timedelta(seconds=total_time)
    future = tomorrow.strftime('%Y-%m-%d %I-%M %p')
    today = datetime.utcnow()
    future_day = tomorrow.strftime("%d")
    future_hour = tomorrow.strftime("%I")
    future_minute = tomorrow.strftime("%M")
    future_year = tomorrow.strftime("%Y")
    future_month = tomorrow.strftime("%m")
    future_second = tomorrow.strftime("%S")
    today_second = today.strftime("%S")
    today_year = today.strftime("%Y")
    today_month = today.strftime("%m")
    today_day = today.strftime("%d")
    today_hour = today.strftime("%I")
    today_minute = today.strftime("%M")
    a = datetime(int(future_year), int(future_month), int(future_day),
                 int(future_hour),
                 int(future_minute), int(future_second))
    b = datetime(int(today_year), int(today_month), int(today_day), int(today_hour),
                 int(today_minute), int(today_second))
    ce = a - b

    d = str(ce).split()


    db.child("Cooldown").child("coolDown").child(message).update({
        "year": future_year,
        "month": future_month,
        "day": future_day,
        "hour": future_hour,
        "minute": future_minute,
        "second": future_second
    })