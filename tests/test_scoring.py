import servidor


def test_calcular_puntos_unique():
    jugadores = {
        'p1': {'respuestas': {'nombre': 'Ana'}},
        'p2': {'respuestas': {'nombre': 'Bea'}},
    }
    puntajes = servidor.calcular_puntos_ronda(jugadores)
    assert puntajes['p1'] == 100
    assert puntajes['p2'] == 100


def test_calcular_puntos_duplicate():
    jugadores = {
        'p1': {'respuestas': {'nombre': 'Ana'}},
        'p2': {'respuestas': {'nombre': 'Ana'}},
        'p3': {'respuestas': {'nombre': ''}},
    }
    puntajes = servidor.calcular_puntos_ronda(jugadores)
    assert puntajes['p1'] == 50
    assert puntajes['p2'] == 50
    assert puntajes['p3'] == 0