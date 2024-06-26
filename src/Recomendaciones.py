import json
import os
import joblib
import pandas as pd

from Steam import obtener_tags_por_steam_appid

def get_recommended_games(lista_juegos):
    vectorizer = joblib.load('vectorizer.pkl')
    kmeans = joblib.load('kmeans.pkl')
    current_directory = os.path.dirname(__file__)
    df = pd.read_excel(os.path.join(current_directory, '..', 'dataset', 'games_clustered.xlsx'))
    recommended_games = []
    for juego in lista_juegos:
        tags_obtenidos = obtener_tags_por_steam_appid(str(juego['name']))

        X = vectorizer.transform([tags_obtenidos])
        cluster = kmeans.predict(X)

        print(f"El juego {juego['name']} pertenece al cluster {cluster[0]}")
        print(json.dumps(juego, indent=4))

        # Obtener los juegos en el mismo cluster
        mismo_cluster = df[df['Cluster'] == cluster[0]]

        # Definir una ventana de clusters cercanos
        window = 5

        # Obtener los juegos en los clusters cercanos
        clusters_cercanos = range(cluster[0] - window, cluster[0] + window + 1)
        otros_clusters = df[df['Cluster'].isin(clusters_cercanos)]

        # Combinar los juegos del cluster principal y los clusters cercanos
        juegos_combinados = pd.concat([mismo_cluster, otros_clusters])

        # Filtrar los juegos únicos
        juegos_combinados = juegos_combinados.drop_duplicates(subset=['Name'])

        # Seleccionar los juegos del mismo cluster hasta alcanzar la cantidad deseada
        num_juegos_adicionales = 11  # Restar 1 para ajustar el número de juegos
        juegos_adicionales = mismo_cluster.sample(n=min(num_juegos_adicionales, len(mismo_cluster)))

        # Si la cantidad de juegos del mismo cluster es menor que la deseada,
        # completar con juegos de otros clusters cercanos
        num_juegos_adicionales_faltantes = num_juegos_adicionales - len(juegos_adicionales)
        if num_juegos_adicionales_faltantes > 0:
            otros_juegos = otros_clusters.sample(n=num_juegos_adicionales_faltantes)
            juegos_adicionales = pd.concat([juegos_adicionales, otros_juegos])
        
        # Almacenar nombres de juegos únicos temporalmente en un conjunto
        juegos_unicos_temp = set()

        # Agregar nombres de juegos del mismo cluster al conjunto temporal
        for _, recommendedGame in juegos_adicionales.iterrows():
            juegos_unicos_temp.add(recommendedGame['Name'])

        # Eliminar el juego actual de la lista de recomendados
        juegos_unicos_temp.discard(juego['name'])

        print(f"Juegos recomendados para {juego['name']}:")
        print(juegos_unicos_temp)  # Imprimir nombres únicos de juegos

        # Agregar juegos únicos del conjunto temporal a la lista final
        recommended_games.extend(list(juegos_unicos_temp))

    return recommended_games


