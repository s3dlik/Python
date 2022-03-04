import matplotlib.pyplot as plt
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .connectionHeader import *
from faceitStats.models import Account


# Create your views here.
def index(request):
    account = Account.objects.all()
    account_num = Account.objects.all().count()
    url = account.model.accountUrl
    level = account.model.level
    photo = account.model.avatar

    context = {
        'account' : account,
        'account_num' : account_num,
        'url' : url,
        'avatar' : photo,
        'level':level,
    }

    return render(request, 'faceitStats/index.html', context=context)


def accountDetails(request, account_id, map=None):
    try:
        #returns exact account
        acc = get_object_or_404(Account, pk=account_id)

        #returs player ID, need that for next api request
        player_id = returnPlayerID(acc.accountUrl)

        details = getDetailsHeader(acc.accountUrl)

        lifetimeData = getMatchesInformationAll(player_id)
        maps = returnMaps(player_id)
        map_details = returnMatchesInfo(request,player_id, map)

        #return graph
        graph = returnGraph(player_id)

        return render(request, 'faceitStats/accountDetails.html', {'acc': acc, 'details': details,'lifetime' : lifetimeData, 'Maps': maps, 'map_details':map_details, 'graph':graph})
    except Account.DoesNotExist:
        raise Http404('User with that nickname does not exist on Faceit!')



def accountDetailsPost(request):
    try:
        if request.method == "POST":
            try:
                accID = request.POST['acc-id']
                maps = request.POST['map_name']
                return accountDetails(request, accID, maps)
            except:
                raise Http404('No map!')
    except Account.DoesNotExist:
        raise Http404('User with that nickname does not exist on Faceit!')

def getDetailsHeader(nickname):
    data = retrieveDataByNick(nickname)
    player_id = data['player_id']
    steamID = data['games']['csgo']['game_player_id']
    name = data['nickname']
    level = data['games']['csgo']['skill_level']
    elo = data['games']['csgo']['faceit_elo']
    membership = data['membership_type']
    dict = {
        'Nickname' : name,
        'Elo' : elo,
        'SteamID' : steamID,
        'Membership' : membership,
        'Level': level,
        'Player_id': player_id
    }
    return dict


#data ze vsech zapasu
def getMatchesInformationAll(id):

    data = retrieveDataByID(id)

    gamesNum = data['lifetime']['Matches']
    currentWinStreak = data['lifetime']['Current Win Streak']
    winRate = data['lifetime']['Win Rate %']
    avgKD = data['lifetime']['Average K/D Ratio']
    winsCount = data['lifetime']['Wins']
    avgHS = data['lifetime']['Average Headshots %']
    longetWinStreak = data['lifetime']['Longest Win Streak']
    recentResults = data['lifetime']['Recent Results']
    dict = {
        'Number of games' : gamesNum,
        'Current win streak':currentWinStreak,
        'Win rate': winRate,
        'Average kills/deaths' : avgKD,
        'Wins count' : winsCount,
        'Average headshots' : avgHS,
        'Longest win streak' : longetWinStreak,
        'Recent results' : recentResults,
    }
    return dict

def returnMaps(playerid):

    data = retrieveDataByID(playerid)
    segments = data['segments']
    list = []
    for elemI in segments:
        if elemI['mode'] == '5v5':
            if elemI not in list:
                list.append(elemI['label'])
    return list
#toto bych taky nechal, vrati mi to ID hrace, nevim jak jinak bych to udelal
def returnPlayerID(nickname):

    data = retrieveDataByNick(nickname)
    player_id = data['player_id']

    return player_id
#toto bych nechal, vraci mi to udaje ohledne zapasu na dane mape
def returnMatchesInfo(request,playerid, map_name):

    data = retrieveDataByID(playerid)
    segments = data['segments']
    if map_name is not None:
        for elemI in segments:
            if elemI['mode'] == '5v5':
                if elemI['label'] == map_name:
                    matches = elemI['stats']['Matches']
                    kills = elemI['stats']['Kills']
                    MPVS = elemI['stats']['MVPs']
                    hs = elemI['stats']['Headshots']
                    wins = elemI['stats']['Wins']
                    deaths = elemI['stats']['Deaths']
                    winRate = elemI['stats']['Win Rate %']
                    img = elemI['img_regular']
                    assists = elemI['stats']['Assists']
        loses = int(matches) - int(wins)
        dict= {
            'Image': img,
            'Total matches' : matches,
            'Total kills': kills,
            'Total deaths': deaths,
            'Total headshots': hs,
            'Total assists' : assists,
            'Total MVPs' : MPVS,
            'Total wins' : wins,
            'Total loses' : loses,
            'Win rate' : winRate

        }
        return dict
    return None
#TOTO JE OK
def addAccount(request):
    if request.method == 'POST':
        account = Account.objects.all()
        account_form = Account(accountUrl=request.POST.get('nickname'))


        res = connectionReq(account_form.accountUrl)
        for ele in account:
            if ele.accountUrl == account_form.accountUrl:
                messages.error(request,'This user is already in users list!')
                return redirect('/')
        if res.status_code == 200:
            data = res.json()
            game = data['games']
            for ele in game:
                if ele == 'csgo':
                    messages.success(request,"User added to player list!")
                    account_form.save()
                else:
                    messages.error(request,"This user is not playing CSGO!")
                    return redirect('/')
        else:
            messages.error(request, "This user does not exist on faceit!")
            return redirect('/')
        account_form.avatar = data['avatar']
        account_form.level = data['games']['csgo']['skill_level']
        account_form.save()
        return redirect('/')
# toto je OK
def returnGraph(player_id):
    try:
        data = retrieveDataByID(player_id)
        segments = data['segments']
        steamid = data['player_id']
        listTmp = []
        for ele in segments:
            for tmp in ele:
                if ele['mode'] == '5v5':
                    if tmp == 'stats':
                        dict = {
                            ele['label']: ele[tmp]['Kills']
                            }
                        listTmp.append(dict)

        x_tmp = []
        y_tmp = []
        for i in listTmp:
            for tmp in i:
                x_tmp.append(tmp)

        for i in listTmp:
            for tmp in i:
                y_tmp.append(i[tmp])

        y_tmp_to_int = map(int, y_tmp)
        list_y_tmp_to_int = list(y_tmp_to_int)

        xSize = len(x_tmp)
        ySize = len(y_tmp)
        fig = plt.figure(figsize=(xSize, ySize))
        ax = fig.add_subplot()
        fig.suptitle('All kills on all maps', fontsize=14, fontweight='bold')
        fig.set_figheight(5)
        fig.set_figwidth(10)
        fig.autofmt_xdate()
        ax.plot(x_tmp, list_y_tmp_to_int, 'ro-')
        ax.set_xlabel('Maps')
        ax.set_ylabel('Kills')

        return fig.savefig('faceitStats/static/style/images/graphs/'+steamid,dpi=fig.dpi)
    except :
        raise Http404('null')





