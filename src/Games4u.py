import pandas as pd
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Leer el archivo Excel y convertirlo en una lista de diccionarios
current_directory = os.path.dirname(__file__)

# Construye la ruta al archivo Excel en la carpeta 'dataset'
directory_games= os.path.join(current_directory, '..', 'dataset', 'games.xlsx')

df = pd.read_excel(directory_games)

directory_cluster= os.path.join(current_directory, '..', 'dataset', 'games_clustered.xlsx')

df_cluster = pd.read_excel(directory_cluster)

videojuegos_cluster = df_cluster.to_dict('records')

videojuegos = df.to_dict('records')

@app.route('/')
def index():
    # Pasar la lista de videojuegos a la plantilla
    return render_template('index.html', videojuegos=videojuegos)

@app.route('/recomendacion', methods=['POST'])
def recomendacion():
    juegos_favoritos = request.form.getlist('juegos_gustados')
    
    # Crear un diccionario que mapea cada juego favorito a los juegos recomendados del mismo cluster
    recomendaciones = {}
    for i in juegos_favoritos:
        nombre_juego = videojuegos_cluster[int(i)]['Name']
        cluster_juego = videojuegos_cluster[videojuegos_cluster['Name'] == nombre_juego]['Cluster'].values[0]
        juegos_recomendados = videojuegos_cluster[videojuegos_cluster['Cluster'] == cluster_juego]['Name'].tolist()
        recomendaciones[nombre_juego] = juegos_recomendados
    
    # Verificar si se encontraron juegos recomendados
    if recomendaciones:
        return render_template('recomendacion.html', recomendaciones=recomendaciones)
    else:
        return "No se encontraron juegos recomendados."

if __name__ == '__main__':
    app.run(debug=True)