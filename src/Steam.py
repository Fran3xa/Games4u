import joblib
import os
import json
import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from steam_web_api import Steam
from sklearn.decomposition import TruncatedSVD
from ProcesoText import preprocess_text

# Clave de Steam proporcionada para acceder a su API
STEAM_KEY = 'E54AABAFEDCB6F054775D23856674223'

# Id del usuario de Steam (debe tener el perfil público)
STEAM_USER_ID2 = '76561198118719571'

steam = Steam(STEAM_KEY)

# Obtener detalles del usuario de Steam
user_details = steam.users.get_user_details(STEAM_USER_ID2)

# Obtener los juegos propiedad del usuario de Steam
owned_games = steam.users.get_owned_games(STEAM_USER_ID2)
games_list = owned_games['games']
sorted_games = sorted(games_list, key=lambda x: x["playtime_forever"], reverse=True)
most_played_games = sorted_games[:5]

# Lista para almacenar descripciones de los juegos del usuario
user_game_descriptions = []

# Obtener detalles de los juegos y sus géneros
for game in most_played_games:
    game_details = steam.apps.get_app_details(int(game['appid']))
    result = game_details[str(game['appid'])]["data"]
    game_details2 = steam.apps.get_app_details(int(game['appid']), filters='genres')
    genres = game_details2[str(game['appid'])]["data"]["genres"]
    
    game_info = {
        "name": result["name"],
        "steam_appid": result["steam_appid"],
        "short_description": result["short_description"],
        "header_image": result["header_image"],
        "genres": ", ".join(genre["description"] for genre in genres)
    } 
    user_game_descriptions.append(game_info)

# Leer el archivo Excel con los juegos clusterizados
current_directory = os.path.dirname(__file__)
df = pd.read_excel(os.path.join(current_directory, '..', 'dataset', 'games_clustered.xlsx'))

primer_juego = user_game_descriptions[0]

# Cargar vectorizador y modelo de clustering
vectorizer = joblib.load('vectorizer.pkl')
kmeans = joblib.load('kmeans.pkl')
hvectorizer = joblib.load('hashing_vectorizer.pkl')


# Preprocesar la descripción del primer juego
caracteristicas_transformadas = preprocess_text(primer_juego['short_description'])
genero_primer_juego = primer_juego['genres']
X = vectorizer.transform([caracteristicas_transformadas])
genero_transformado = hvectorizer.transform([genero_primer_juego])
caracteristicas_primer_juego = sp.hstack([X, genero_transformado])


# Predicción del cluster del primer juego
cluster = kmeans.predict(caracteristicas_primer_juego)

print(f"El juego {primer_juego['name']} pertenece al cluster {cluster[0]}")
print(json.dumps(primer_juego, indent=4))

# Filtrar los juegos que pertenecen al mismo cluster
mismo_cluster = df[df['Cluster'] == cluster[0]]

print("Juegos en el mismo cluster:")
# Imprimir el nombre de cada juego
for _, juego in mismo_cluster.iterrows():
    print(juego['Name'])