import urllib.request
import json
import random
import redis
from setting import api_key


def game_choice(steamid):
    def gameinfo_url(steamid):
        http = "http://"
        base = "api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
        arg = "&format=json&include_appinfo=1&steamid="
        return http + base + api_key + arg + steamid
    url = gameinfo_url(steamid)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf8'))['response']
    gamelist = [game['name'] for game in data['games']]
    random_game = random.choice(gamelist)
    return random_game


def search_id(vanityurl):
    def userinfo_url(vanityurl):
        http = "http://"
        base = "api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key="
        arg = "&vanityurl="
        return http + base + api_key + arg + vanityurl
    url = userinfo_url(vanityurl)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf8'))['response']
    if data['success'] == 1:
        return data['steamid']


if __name__ == "__main__":
    r = redis.StrictRedis()
    r.set('nemo', '76561198137536266')
    my_id = 'pse1202'
    r.set(my_id, search_id(my_id))
    print(game_choice(r.get(my_id).decode('utf8')))
