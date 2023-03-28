import requests
import json
import csv
import time

municipality = "ZWD01"

baseurl = "https://www.wozwaardeloket.nl/wozwaardeloket-api/v1/wozwaarde/wozobjectnummer/{}"

def gettoken():
    url = "https://www.wozwaardeloket.nl/wozwaardeloket-api/v1/session/start"
    response = requests.post(url=url)
    lb_sticky = response.cookies.get_dict().get("LB_STICKY")
    session = response.cookies.get_dict().get("SESSION")
    return lb_sticky, session


sticky, session = gettoken()


with open("wozobjects_{}.csv".format(municipality)) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        url = baseurl.format(row[0])
        cookie = "LB_STICKY={}; SESSION={};".format(sticky, session)
        headers = {"Cookie": cookie}
        retry = True
        while retry:
            try:
                response = requests.get(url=url, headers=headers)
                if response.status_code == 429:
                    time.sleep(2)
                else:
                    wozbject = response.json().get("wozObject")
                    wozwaarde = response.json().get("wozWaarden")
                    print (wozwaarde)
                    retry = False
            except Exception as e:
                time.sleep(1)



