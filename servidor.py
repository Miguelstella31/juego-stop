from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random
import string

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

jugadores = {}
letra_actual = ''
expected_players = None

def nueva_letra():
    return random.choice(string.ascii_uppercase)

def comenzar_ronda():
    global letra_actual
    letra_actual = nueva_letra()
    socketio.emit('letra', letra_actual, broadcast=True)

@app.route('/')
def index():
    global expected_players
    count = request.args.get('count', type=int)
    if count:
        expected_players = count
    return render_template('index.html', expected_players=expected_players)

@socketio.on('unirse')
def unirse(data):
    nombre = data['nombre']
    jugadores[nombre] = {'puntos': 0}
    emit('jugadores_actualizados', jugadores, broadcast=True)
    if expected_players:
        if len(jugadores) < expected_players:
            socketio.emit('esperando',
                           {'actual': len(jugadores), 'esperados': expected_players},
                           broadcast=True)
        elif len(jugadores) == expected_players:
            comenzar_ronda()

@socketio.on('nueva_ronda')
def iniciar_ronda():
    comenzar_ronda()

@socketio.on('enviar_respuestas')
def recibir_respuestas(data):
    nombre = data['nombre']
    respuestas = data['respuestas']
    puntos = sum(10 for r in respuestas.values() if r.strip() != '')
    jugadores[nombre]['puntos'] += puntos
    emit('jugadores_actualizados', jugadores, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5050)
