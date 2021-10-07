from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, response
import requests

# Create your views here.

API_KEY = 'RGAPI-617c8d8f-b131-446b-8eec-b0f852ea8a98'

def ok(request):
    return render(request, 'ok.htm')

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
    summonersLeague = SummonerByLeague()
    

    for index, summoner in enumerate(summonersLeague['entries']):
        puuid =  SummonerByName(summoner['summonerName'])['puuid']
        if index == 10:
            break
        else:
            urlMatches = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100&api_key={API_KEY}"
            response = requests.get(urlMatches).json()
            print(response)
    
    return HttpResponse('Holi xD')
    


