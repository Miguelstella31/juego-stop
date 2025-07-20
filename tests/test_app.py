import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from servidor import app, socketio, jugadores


def test_unirse_event():
    jugadores.clear()
    client = socketio.test_client(app)
    client.emit('unirse', {'nombre': 'Jugador1'})
    client.emit('unirse', {'nombre': 'Jugador2'})
    assert 'Jugador1' in jugadores
    assert 'Jugador2' in jugadores
    client.disconnect()


def test_index_route():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
