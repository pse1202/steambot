import urllib.request
import json
import random
key = open('steamapi_key', 'r').read()[:-1]
nemo = "76561198137536266"


def game_choice(steamid):
    def gameinfo_url(steamid):
        http = "http://"
        base = "api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
        arg = "&format=json&include_appinfo=1&steamid="
        return http + base + key + arg + steamid
    url = gameinfo_url(steamid)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf8'))
    gamelist = [game['name'] for game in data['response']['games']]
    random_game = random.choice(gamelist)
    return random_game

if __name__ == "__main__":
    print(game_choice(nemo))
