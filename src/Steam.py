# En este archivo usaremos la clave de Steam para poder extraer juegos de las cuentas de usuario
# y asi recomendarle en base a sus últimos juegos jugados
import json
import os
import joblib
from steam_web_api import Steam
import pandas as pd

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
STEAM_KEY = 'E54AABAFEDCB6F054775D23856674223'

# Id del usuario de Steam, este tiene que tener el perfil publico para poder usarlo
#STEAM_USER_ID = '76561199028403880'
# Este usuario contiene una biblioteca mas extensa de videojuegos jugados
#STEAM_USER_ID2 = '76561198118719571'

steam = Steam(STEAM_KEY)

#user_details = steam.users.get_user_details(STEAM_USER_ID2)
def get_most_played_games(user_id):


    owned_games = steam.users.get_owned_games(user_id)

    # Organizamos todos los juegos en funcion de su tiempo jugado, y nos quedamos con los 5 mas jugados
    games_list = owned_games['games']
    sorted_games = sorted(games_list, key=lambda x: x["playtime_forever"], reverse=True)

    user_game_descriptions = []

    for game in sorted_games:
        # Obtener los datos del juego
        game_details = steam.apps.get_app_details(int(game['appid']))
        result = game_details[str(game['appid'])]["data"]

        # Obtener las descripciones de los géneros
        game_details2 = steam.apps.get_app_details(int(game['appid']),
                                                filters = 'genres')
        genres = game_details2[str(game['appid'])]["data"]["genres"]
        
        game_info = {
            "name": result["name"],
            "steam_appid": result["steam_appid"],
            "short_description": result["short_description"],
            "header_image": result["header_image"],
            "genres": ", ".join(genre["description"] for genre in genres)
        } 
        user_game_descriptions.append(game_info)

    return user_game_descriptions

