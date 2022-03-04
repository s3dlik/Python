import requests

def retrieveDataByID(id):
    url = "https://open.faceit.com/data/v4/players/" + id + "/stats/csgo"
    headers = {
        'Authorization': 'Your token here',
        'accept': 'application/json'
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    return data

def retrieveDataByNick(nickname):
    url = "https://open.faceit.com/data/v4/players?nickname=" + nickname
    headers = {
        'Authorization': 'Your token here',
        'accept': 'application/json'
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    return data

def connectionReq(nick):
    url = "https://open.faceit.com/data/v4/players?nickname=" + nick

    headers = {
        'Authorization': 'Your token here',
        'accept': 'application/json'
    }
    res = requests.get(url,headers=headers)
    return res