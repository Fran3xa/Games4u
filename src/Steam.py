# En este archivo usaremos la clave de Steam para poder extraer juegos de las cuentas de usuario
# y asi recomendarle en base a sus últimos juegos jugados
import json
from steam_web_api import Steam

# Clave de Steam proporcionado para acceder a su API
STEAM_KEY = 'E54AABAFEDCB6F054775D23856674223'

# Id del usuario de Steam, este tiene que tener el perfil publico para poder usarlo
STEAM_USER_ID = '76561199028403880'
# Este usuario contiene una biblioteca mas extensa de videojuegos jugados
STEAM_USER_ID2 = '76561198118719571'

steam = Steam(STEAM_KEY)

user_details = steam.users.get_user_details(STEAM_USER_ID2)

owned_games = steam.users.get_owned_games(STEAM_USER_ID2)

# Organizamos todos los juegos en funcion de su tiempo jugado, y nos quedamos con los 5 mas jugados
games_list = owned_games['games']
sorted_games = sorted(games_list, key=lambda x: x["playtime_forever"], reverse=True)

most_played_games = sorted_games[:5]

#for game in most_played_games:
#    print(json.dumps(game, indent=4))
 
# Una vez obtenidos los 5 juegos mas jugados por el usuario, obtenemos los detalles del juego
user_game_descriptions = []

for game in most_played_games:
    game_details = steam.apps.get_app_details(int(game['appid']))
    result = game_details[str(game['appid'])]["data"]
    game_info = {
        "name": result["name"],
        "steam_appid": result["steam_appid"],
        "short_description": result["short_description"],
        "header_image": result["header_image"]
    } 
    user_game_descriptions.append(game_info)

#for game in user_game_descriptions:
#   print(json.dumps(game, indent=4))