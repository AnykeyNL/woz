import requests
import csv

municipality = "ZTM00"

url = "https://www.wozwaardeloket.nl/wozwaardeloket-api/v1/suggest/kadastraal?gemeente={}&sectie={}&perceel={}&page=0&size=100"

data_file = open("wozobjects_{}.csv".format(municipality), 'w')
csv_writer = csv.writer(data_file)

count = 0
with open("parcel_{}.csv".format(municipality)) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reade
        surl = url.format(row[0], row[1], row[2])
        print (surl)
        response = requests.get(url=surl)
        print (response.text)
        docs = response.json().get("docs")
        for wozobject in docs:
            csv_writer.writerow(wozobject.values())





