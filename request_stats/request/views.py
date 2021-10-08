from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, response
from pandas.core.frame import DataFrame
import requests
import pandas as pd
import time

# Create your views here.

API_KEY = 'RGAPI-8af9804e-23b1-4996-a294-517e4b29989f'

def ok(request):
    return 

def getSummonerByName(request = None):
    summonerName = 'GeneralSn1per'
    
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={API_KEY}"
    response = requests.get(url).json()
    return JsonResponse(response)

def SummonerByName(summonerName):
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={API_KEY}"
    response = requests.get(url).json()
    return response

def getSummonerByLeague(request = None):
    url = f"https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={API_KEY}"
    response = requests.get(url).json()
    return JsonResponse(response)

def SummonerByLeague():
    url = f"https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={API_KEY}"
    response = requests.get(url).json()
    return response

def getMatches(request):
    urlMatch = f""
    summonersLeague = SummonerByLeague()
    urlMatch = f"https://americas.api.riotgames.com/lol/match/v5/matches/"
    
    data = pd.DataFrame()
    for index, summoner in enumerate(summonersLeague['entries']):
        puuid =  SummonerByName(summoner['summonerName'])['puuid']
        if index == 1:
            break
        else:
            urlByPuuid = f"{urlMatch}by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}"
            response = requests.get(urlByPuuid).json()
            for i, match in enumerate(response):
                urlByMatchId = f"{urlMatch}{match}?api_key={API_KEY}"
                matchStatsResponse = requests.get(urlByMatchId).json()
                if i == 20:
                    break
                else:
                    teams = matchStatsResponse['info']['teams']
                    dataTeams = []
                    for team in teams:
                        dataTeam = {
                        'idTeam': None,
                        'firstBaron': None,
                        'killsBaron': None,
                        'firstChampion': None,
                        'killsChampion': None,
                        'firstDragon': None,
                        'killsDragon': None,
                        'firstInhibitor': None,
                        'killsInhibitor': None,
                        'firstRiftHerald': None,
                        'killsRiftHerald': None,
                        'firstTower': None,
                        'killsTower': None,
                        'win': None,
                    }
                        dataTeam['idTeam'] = team['teamId']
                        dataTeam['win'] = team['win']
                        objectives = team['objectives']
                        dataTeam['firstBaron'] = objectives['baron']['first']
                        dataTeam['killsBaron'] = objectives['baron']['kills']
                        dataTeam['firstChampion'] = objectives['champion']['first']
                        dataTeam['killsChampion'] = objectives['champion']['kills']
                        dataTeam['firstDragon'] = objectives['dragon']['first']
                        dataTeam['killsDragon'] = objectives['dragon']['kills']
                        dataTeam['firstInhibitor'] = objectives['inhibitor']['first']
                        dataTeam['killsInhibitor'] = objectives['inhibitor']['kills']
                        dataTeam['firstRiftHerald'] = objectives['riftHerald']['first']
                        dataTeam['killsRiftHerald'] = objectives['riftHerald']['kills']
                        dataTeam['firstTower'] = objectives['tower']['first']
                        dataTeam['killsTower'] = objectives['tower']['kills']
                        dataTeams.append(dataTeam)
                    df = pd.DataFrame(dataTeams)
                    data = pd.concat([df,data])
    print(data)
                
    
    return JsonResponse(matchStatsResponse)

    # [   
    #     {
    #         'idTeam': 123,
    #         'firstBaron': True,
    #         'killsBaron': 2,
    #     },
    #     {
    #         'idTeam': 456,
    #         'firstBaron': False, 
    #         'killsBaron': 0,
    #     }
    # ]
    


