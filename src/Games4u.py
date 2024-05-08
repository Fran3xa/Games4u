from flask import Flask, redirect, render_template, request, jsonify, url_for
import Steam
import json
import Recomendaciones

app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def index():
    # Pasar la lista de videojuegos a la plantilla
    return render_template('index.html')

@app.route('/busqueda')
def busqueda():
    return render_template('busqueda.html')

@app.route('/UsuarioInfo')
def usuarioInfo():
    games_played = request.args.get('games_played')
    user_info = request.args.get('user_id')

    game_info_list = json.loads(games_played)
    user_info_list = json.loads(user_info)

    # Aquí construyes cada juego en el formato deseado
    formatted_games = []
    for game in game_info_list:
        formatted_game = {
            "name": game["name"],
            "steam_appid": game["steam_appid"],
            "short_description": game["short_description"],
            "header_image": game["header_image"],
            "genres": game["genres"]
        }
        formatted_games.append(formatted_game)

    formatted_users = []
    for user in user_info_list:
        formatted_user = {
            "name": user["name"],
            "steamid": user["steamid"],
            "avatar": user["avatar"]
        }
        formatted_users.append(formatted_user)
    return render_template('UsuarioInfo.html', games_played=formatted_games, userInfo = formatted_users)

@app.route('/get_games', methods=['POST'])
def get_games():
    user_id = request.form.get('userid')
    most_played_games = Steam.get_most_played_games(user_id)
    userInfo = Steam.get_user_details(user_id)
    return redirect(url_for('usuarioInfo', games_played=json.dumps(most_played_games), user_id = json.dumps(userInfo)))

@app.route('/save_recommendations', methods=['POST'])
def save_recommendations():
    games = request.get_json()
    juegos_recomendados = Recomendaciones.get_recommended_games(games)
    print(juegos_recomendados)
    return jsonify(juegos_recomendados)

@app.route('/recomendacion', methods=['POST'])
def recomendacion():
    selected_game = request.form.get('selected_game')
    print(selected_game)
    return render_template('recomendacion.html')

if __name__ == '__main__':
    app.run(debug=True)