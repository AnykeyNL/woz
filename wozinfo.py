import requests
import json
import csv
import time

municipality = "ZWD01"

baseurl = "https://www.wozwaardeloket.nl/wozwaardeloket-api/v1/wozwaarde/wozobjectnummer/{}"

data_file = open("wozinfo_{}.csv".format(municipality), 'w')
csv_writer = csv.writer(data_file)

def gettoken():
    url = "https://www.wozwaardeloket.nl/wozwaardeloket-api/v1/session/start"
    response = requests.post(url=url)
    lb_sticky = response.cookies.get_dict().get("LB_STICKY")
    session = response.cookies.get_dict().get("SESSION")
    return lb_sticky, session


sticky, session = gettoken()

objects = 0
s = 0

with open("wozobjects_{}.csv".format(municipality)) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        url = baseurl.format(row[0])
        cookie = "LB_STICKY={}; SESSION={};".format(sticky, session)
        headers = {"Cookie": cookie}
        retry = True
        while retry:
            try:
                print ("getting: {}".format(url))
                response = requests.get(url=url, headers=headers)
                if response.status_code == 429:
                    print ("Refresh token...")
                    sticky, session = gettoken()
                    cookie = "LB_STICKY={}; SESSION={};".format(sticky, session)
                    headers = {"Cookie": cookie}
                else:
                    objects = objects + 1
                    wozobject = response.json().get("wozObject")
                    wozwaarde = response.json().get("wozWaarden")
                    waarde = [0,0,0,0,0,0,0,0,0]
                    for w in wozwaarde:
                        if "2022" in w["peildatum"] :
                            waarde[0] = w["vastgesteldeWaarde"]
                        if "2021" in w["peildatum"] :
                            waarde[1] = w["vastgesteldeWaarde"]
                        if "2020" in w["peildatum"] :
                            waarde[2] = w["vastgesteldeWaarde"]
                        if "2019" in w["peildatum"] :
                            waarde[3] = w["vastgesteldeWaarde"]
                        if "2018" in w["peildatum"] :
                            waarde[4] = w["vastgesteldeWaarde"]
                        if "2017" in w["peildatum"] :
                            waarde[5] = w["vastgesteldeWaarde"]
                        if "2016" in w["peildatum"] :
                            waarde[6] = w["vastgesteldeWaarde"]
                        if "2015" in w["peildatum"] :
                            waarde[7] = w["vastgesteldeWaarde"]
                        if "2014" in w["peildatum"]:
                            waarde[8] = w["vastgesteldeWaarde"]

                    print (waarde)
                    print ("count: {}".format(objects))
                    wozobject['2022'] = waarde[0]
                    wozobject['2021'] = waarde[1]
                    wozobject['2020'] = waarde[2]
                    wozobject['2019'] = waarde[3]
                    wozobject['2018'] = waarde[4]
                    wozobject['2017'] = waarde[5]
                    wozobject['2016'] = waarde[6]
                    wozobject['2015'] = waarde[7]
                    wozobject['2014'] = waarde[8]

                    csv_writer.writerow(wozobject.values())
                    retry = False
            except Exception as e:
                print (e)
                time.sleep(2)



