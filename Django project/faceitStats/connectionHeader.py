import requests

def retrieveDataByID(id):
    url = "https://open.faceit.com/data/v4/players/" + id + "/stats/csgo"
    headers = {
        'Authorization': 'Bearer 207ad3f2-90bc-4456-b0e9-d4592cbbb566',
        'accept': 'application/json'
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    return data

def retrieveDataByNick(nickname):
    url = "https://open.faceit.com/data/v4/players?nickname=" + nickname
    headers = {
        'Authorization': 'Bearer 207ad3f2-90bc-4456-b0e9-d4592cbbb566',
        'accept': 'application/json'
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    return data

def connectionReq(nick):
    url = "https://open.faceit.com/data/v4/players?nickname=" + nick

    headers = {
        'Authorization': 'Bearer 207ad3f2-90bc-4456-b0e9-d4592cbbb566',
        'accept': 'application/json'
    }
    res = requests.get(url,headers=headers)
    return res