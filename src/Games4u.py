from flask import Flask, render_template, request

app = Flask(__name__)

# Lista de videojuegos (nombre, género)
videojuegos = [
    {"nombre": "The Legend of Zelda: Breath of the Wild", "genero": "Aventura"},
    {"nombre": "Super Mario Odyssey", "genero": "Plataforma"},
    {"nombre": "Red Dead Redemption 2", "genero": "Acción/Aventura"},
    {"nombre": "The Witcher 3: Wild Hunt", "genero": "RPG"},
    {"nombre": "Dark Souls III", "genero": "RPG"},
    {"nombre": "Overwatch", "genero": "FPS"}
]

@app.route('/')
def index():
    return render_template('index.html', videojuegos=videojuegos)

@app.route('/saludo', methods=['GET', 'POST'])
def saludo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        return render_template('saludo.html', nombre=nombre)
    return render_template('formulario.html')

@app.route('/recomendacion', methods=['POST'])
def recomendacion():
    juegos_gustados = request.form.getlist('juegos_gustados')
    
    # Aquí podrías implementar tu algoritmo de recomendación
    # Por ahora, simplemente devolveré los géneros de los juegos seleccionados
    generos_gustados = [videojuegos[int(i)]['genero'] for i in juegos_gustados]

    # Filtrar videojuegos por género
    juegos_recomendados = [juego for juego in videojuegos if juego['genero'] in generos_gustados]

    return render_template('recomendacion.html', juegos_recomendados=juegos_recomendados)

if __name__ == '__main__':
    app.run(debug=True)
