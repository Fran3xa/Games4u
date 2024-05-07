from flask import Flask, render_template, request
import Steam
import Recomendaciones

app = Flask(__name__)

@app.route('/')
def index():
    # Pasar la lista de videojuegos a la plantilla
    return render_template('index.html')

@app.route('/get_games', methods=['POST'])
def get_games():
    user_id = request.form.get('userid')
    most_played_games = Steam.get_most_played_games(user_id)
    return most_played_games

@app.route('/save_recommendations', methods=['POST'])
def save_recommendations():
    games = request.get_json()
    juegos_recomendados = Recomendaciones.get_recommended_games(games)
    print(juegos_recomendados)
    return juegos_recomendados

if __name__ == '__main__':
    app.run(debug=True)