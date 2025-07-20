# Game and Bot Documentation

This document describes how the STOP game works and how automated bots can interact with it.

## Game Overview

The application is a small Flask web server that uses WebSockets via **Flask-SocketIO** for real-time communication. Players connect through their browser and join a shared game lobby.

### Main Features

- **Joining the game**: players submit a name using the `unirse` SocketIO event.
- **Starting a round**: any player can trigger `nueva_ronda` to pick a random letter for that round.
- **Submitting answers**: clients emit `enviar_respuestas` with their words for each category. The server validates that each answer starts with the active letter.
- **Scoring**: the server calls `calcular_puntos_ronda` to award 100 points for unique answers and 50 for duplicates. Scores accumulate across rounds.
- **Real-time updates**: every time answers are processed or a new round starts, the `jugadores_actualizados` event broadcasts the updated scoreboard to all participants.

The front-end located in `templates/index.html` and `static/script.js` implements a minimal interface where these events are used. The main server logic resides in `servidor.py`.

## Bot Clients

Bots can be implemented to play automatically by connecting to the same SocketIO events. The following Python snippet demonstrates the core idea using the `python-socketio` client library (already included in `requirements.txt`):

```python
import socketio

sio = socketio.Client()

@sio.event
def connect():
    sio.emit('unirse', {'nombre': 'Bot'})

@sio.on('letra')
def on_letra(letter):
    # Fill categories automatically when a new letter arrives
    respuestas = {
        'nombre': f'Nombre{letter}',
        'apellido': f'Apellido{letter}',
        'ciudad': f'Ciudad{letter}',
        'color': f'Color{letter}',
        'animal': f'Animal{letter}',
    }
    sio.emit('enviar_respuestas', {'nombre': 'Bot', 'respuestas': respuestas})

sio.connect('http://localhost:5050')
sio.wait()
```

This basic bot joins the lobby when the connection is established, waits for the server to announce a letter, and immediately sends back generated answers.

Multiple bots or human players can run simultaneously since all interactions are event-based.
