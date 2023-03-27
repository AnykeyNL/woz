import requests
import json
import csv

municipality = "ZWD01"
url = "https://api.kadastralekaart.com/api/v1/cadastral-municipality/{}".format(municipality)
response = requests.get(url=url)

try:
    sections = response.json().get("kadastralesecties")
except IndexError:
    print ("Error getting sections.")
    exit(1)

data_file = open("parcel_{}.csv".format(municipality), 'w')
csv_writer = csv.writer(data_file)

for section in sections:
    print ("Getting data for {}-{}".format(municipality, section["sectie"]))
    url = "https://api.kadastralekaart.com/api/v1/parcel/{}/{}".format(municipality, section["sectie"])
    response = requests.get(url=url)
    parcels = response.json()
    for parcel in parcels:
        print (parcel)
        csv_writer.writerow(parcel.values())

