import requests
import csv
import time
municipality = "ZWD01"

url = "https://www.wozwaardeloket.nl/wozwaardeloket-api/v1/suggest/kadastraal?gemeente={}&sectie={}&perceel={}&page=0&size=1000"

data_file = open("wozobjects_{}.csv".format(municipality), 'w')
csv_writer = csv.writer(data_file)

line = 0
count = 0
with open("parcel_{}.csv".format(municipality)) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        surl = url.format(row[0], row[1], row[2])
        print ("line:{}   count: {}   - {}".format(line, count, surl))
        retry = True
        while retry:
            try:
                response = requests.get(url=surl)
                docs = response.json().get("docs")
                line = line + 1
                for wozobject in docs:
                    count = count + 1
                    csv_writer.writerow(wozobject.values())
                retry = False
            except Exception as e:
                print ("ERROR: {}".format(e))
                time.sleep(1)