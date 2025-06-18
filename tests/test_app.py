import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import string
import pytest

from servidor import app, socketio, nueva_letra, jugadores


@pytest.fixture(autouse=True)
def clear_state():
    jugadores.clear()
    yield
    jugadores.clear()


def test_index_route():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_nueva_letra_returns_uppercase():
    for _ in range(20):
        letra = nueva_letra()
        assert letra in string.ascii_uppercase
        assert len(letra) == 1


def test_unirse_adds_player():
    client = socketio.test_client(app)
    client.emit('unirse', {'nombre': 'Alice'})
    socketio.sleep(0)
    assert 'Alice' in jugadores
    assert jugadores['Alice']['puntos'] == 0
    client.disconnect()


def test_recibir_respuestas_updates_score():
    client = socketio.test_client(app)
    client.emit('unirse', {'nombre': 'Bob'})
    socketio.sleep(0)
    respuestas = {
        'nombre': 'Ana',
        'apellido': 'Lopez',
        'ciudad': '',
        'color': '',
        'animal': 'gato'
    }
    client.emit('enviar_respuestas', {'nombre': 'Bob', 'respuestas': respuestas})
    socketio.sleep(0)
    assert jugadores['Bob']['puntos'] == 30
    client.disconnect()
