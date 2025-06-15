from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import string

app = Flask(__name__)
socketio = SocketIO(app)

jugadores = {}
letra_actual = ''

def nueva_letra():
    return random.choice(string.ascii_uppercase)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('unirse')
def unirse(data):
    nombre = data['nombre']
    jugadores[nombre] = {'puntos': 0}
    emit('jugadores_actualizados', jugadores, broadcast=True)

@socketio.on('nueva_ronda')
def iniciar_ronda():
    global letra_actual
    letra_actual = nueva_letra()
    emit('letra', letra_actual, broadcast=True)

@socketio.on('enviar_respuestas')
def recibir_respuestas(data):
    nombre = data['nombre']
    respuestas = data['respuestas']
    puntos = sum(10 for r in respuestas.values() if r.strip() != '')
    jugadores[nombre]['puntos'] += puntos
    emit('jugadores_actualizados', jugadores, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
