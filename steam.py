import urllib.request
import json
import random
key = open('steamapi_key', 'r').read()[:-1]


def gameinfo_url(steamid):
    http = "http://"
    base = "api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
    arg = "&format=json&include_appinfo=1&steamid="
    return http + base + key + arg + steamid

nemo = "76561198137536266"
url = gameinfo_url(nemo)
response = urllib.request.urlopen(url)
data = json.loads(response.read().decode('utf8'))
gamelist = [game['name'] for game in data['response']['games']]
random_game = random.choice(gamelist)
print(random_game)
