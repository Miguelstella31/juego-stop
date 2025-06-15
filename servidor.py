from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import string

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

jugadores = {}
letra_actual = ''


def calcular_puntos_ronda(jugadores):
    """Return a dict of round scores for each player based on their
    stored answers in ``jugadores``.

    Answers that are empty or don't start with the current letter are
    ignored. If an answer is unique for its category it is worth 100
    points, otherwise 50.
    """
    # Gather counts of each answer per category
    categoria_conteos = {}
    for datos in jugadores.values():
        for categoria, respuesta in datos.get("respuestas", {}).items():
            if respuesta:
                categoria_conteos.setdefault(categoria, {})
                key = respuesta.strip().lower()
                categoria_conteos[categoria][key] = categoria_conteos[categoria].get(key, 0) + 1

    # Compute score for each player
    puntajes = {}
    for nombre, datos in jugadores.items():
        puntaje = 0
        for categoria, respuesta in datos.get("respuestas", {}).items():
            if not respuesta:
                continue
            key = respuesta.strip().lower()
            if categoria_conteos.get(categoria, {}).get(key, 0) == 1:
                puntaje += 100
            else:
                puntaje += 50
        puntajes[nombre] = puntaje
    return puntajes

def nueva_letra():
    return random.choice(string.ascii_uppercase)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('unirse')
def unirse(data):
    nombre = data['nombre']
    jujugadores[nombre] = {'puntos': 0, 'respuestas': {}, 'puntos_ronda': 0}
    emit('jugadores_actualizados', jugadores, broadcast=True)

@socketio.on('nueva_ronda')
def iniciar_ronda():
    global letra_actual
    letra_actual = nueva_letra()
    for datos in jugadores.values():
        datos['respuestas'] = {}
        datos['puntos_ronda'] = 0
    emit('letra', letra_actual, broadcast=True)

@socketio.on('enviar_respuestas')
def recibir_respuestas(data):
    nombre = data['nombre']
    respuestas = data['respuestas']
    
    # Guardar solo respuestas que comiencen con la letra actual
    procesadas = {}
    for categoria, respuesta in respuestas.items():
        r = respuesta.strip()
        if r.upper().startswith(letra_actual):
            procesadas[categoria] = r
        else:
            procesadas[categoria] = ""

    jugadores[nombre]['respuestas'] = procesadas

    # Recalcular puntajes de la ronda y actualizar acumulados
    nuevos_puntajes = calcular_puntos_ronda(jugadores)
    for jugador, puntaje in nuevos_puntajes.items():
        diff = puntaje - jugadores[jugador].get('puntos_ronda', 0)
        jugadores[jugador]['puntos'] += diff
        jugadores[jugador]['puntos_ronda'] = puntaje
    emit('jugadores_actualizados', jugadores, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5050)
