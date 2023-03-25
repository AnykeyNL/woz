import requests
import json

// https://www.linkedin.com/pulse/howto-wozwaardeloket-met-python-peter-wieringa/?trk=pulse-article_more-articles_related-content-card&originalSubdomain=nl#


def get_address_id(address):
    url = "https://geodata.nationaalgeoregister.nl/locatieserver/v3/suggest"
    params = {"q" : address}
    t = requests.get(url=url, params=params)

    try:
        addressinfo = t.json().get("response").get("docs")[0]
    except IndexError:
        return None

    url = "https://geodata.nationaalgeoregister.nl/locatieserver/v3/lookup"
    params = {"fl": "*", "id": addressinfo["id"]}

    info = requests.get(url=url, params=params)
    try:
        addressdetails = info.json().get("response").get("docs")[0]
    except IndexError:
        return None

    print (addressdetails["gekoppeld_perceel"][0])
    gemeente, sectie, perceel = addressdetails["gekoppeld_perceel"][0].split("-")
    baseurl = "https://www.wozwaardeloket.nl/wozwaardeloket-api/v1/suggest/kadastraal?gemeente={}&sectie={}&perceel={}&page=0&size=25"
    url = baseurl.format(gemeente, sectie, perceel)
    address_wozinfo = requests.get(url=url)

    for o in address_wozinfo.json().get("docs"):
        print (o)








    return ("x")


gemeentes = ["ZTM00", "ZWD01"]

print (get_address_id("Moldaustroom 97, Zoetermeer"))
