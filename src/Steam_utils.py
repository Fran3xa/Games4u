# En este archivo usaremos la clave de Steam para poder extraer juegos de las cuentas de usuario
# y asi recomendarle en base a sus últimos juegos jugados
import json
import os
import joblib
from steam_web_api import Steam
import pandas as pd
from ProcesoText import replace_text

# Leer el archivo Excel
current_directory = os.path.dirname(__file__)
df = pd.read_excel(os.path.join(current_directory, '..', 'dataset', 'games_clustered.xlsx'))

def obtener_tags_por_steam_appid(steam_appid):
    # Buscar el steam_appid en el DataFrame
    juego = df[df['Name'] == steam_appid]
    
    # Verificar si se encontró el juego
    if not juego.empty:
        # Obtener los tags del juego
        tags = juego.iloc[0]['Tags procesados']
        return tags
    else:
        return None

# Clave de Steam proporcionado para acceder a su API
# Leer la clave de Steam desde local.properties
def get_steam_key():
    key_path = os.path.join(current_directory, '..', 'local.properties')
    with open(key_path, 'r') as f:
        for line in f:
            if line.startswith('STEAM_KEY='):
                return line.strip().split('=', 1)[1]
    raise ValueError('STEAM_KEY no encontrado en local.properties')

STEAM_KEY = get_steam_key()

steam = Steam(STEAM_KEY)

def get_user_details(user_id):
    user_details = steam.users.get_user_details(user_id)
    result = []
    user_info = {
        "steamid": user_details["player"]["steamid"],
        "name": user_details["player"]["personaname"],
        "avatar": user_details["player"]["avatar"]
    }
    result.append(user_info)
    return result

def get_most_played_games(user_id):

    owned_games = steam.users.get_owned_games(user_id)

    # Organizamos todos los juegos en funcion de su tiempo jugado, y nos quedamos con los 5 mas jugados
    games_list = owned_games['games']
    sorted_games = sorted(games_list, key=lambda x: x["playtime_forever"], reverse=True)

    user_game_descriptions = []

    for game in sorted_games[:5]:
        # Obtener los datos del juego
        game_details = steam.apps.get_app_details(int(game['appid']))
        result = game_details[str(game['appid'])]["data"]

        # Obtener las descripciones de los géneros
        game_details2 = steam.apps.get_app_details(int(game['appid']),
                                                filters = 'genres')
        genres = game_details2[str(game['appid'])]["data"]["genres"]

        game_details3 = steam.apps.get_app_details(int(game['appid']), filters='metacritic')
        if str(game['appid']) in game_details3 and "metacritic" in game_details3[str(game['appid'])]["data"]:
            metacritic = game_details3[str(game['appid'])]["data"]["metacritic"]["score"]
        else:
            metacritic = 0
        
        game_info = {
            "name": result["name"],
            "steam_appid": result["steam_appid"],
            "short_description": result["short_description"],
            "header_image": result["header_image"],
            "genres": ", ".join(genre["description"] for genre in genres),
            "metacritic": metacritic
        } 
        user_game_descriptions.append(game_info)

    return user_game_descriptions

def get_game_details_id(gameId):
    game_details = steam.apps.get_app_details(int(gameId))
    result = game_details[str(gameId)]["data"]

    game_details2 = steam.apps.get_app_details(int(gameId),
                                                filters = 'genres')
    genres = game_details2[str(gameId)]["data"]["genres"]

    game_details3 = steam.apps.get_app_details(int(gameId), filters='metacritic')
    if str(gameId) in game_details3 and "metacritic" in game_details3[str(gameId)]["data"]:
        metacritic = game_details3[str(gameId)]["data"]["metacritic"]["score"]
    else:
        metacritic = 0

    game_info = {
            "name": result["name"],
            "steam_appid": result["steam_appid"],
            "short_description": result["short_description"],
            "header_image": result["header_image"],
            "genres": ", ".join(genre["description"] for genre in genres),
            "metacritic": metacritic
    }

    game_complete = []
    game_complete.append(game_info)

    return game_complete

def get_game_details_name(gameName):
    gameName = replace_text(gameName)
    game = steam.apps.search_games(gameName)
    if not game['apps']:
        return None
    gameId = game['apps'][0]['id'][0]
    result = get_game_details_id(gameId)
    game_info = {
        "name": result[0]["name"],
        "steam_appid": result[0]["steam_appid"],
        "short_description": result[0]["short_description"],
        "header_image": result[0]["header_image"],
        "genres": result[0]["genres"],
        "metacritic": result[0]["metacritic"]
    }
    return game_info