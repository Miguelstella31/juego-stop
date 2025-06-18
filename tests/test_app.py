import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from servidor import app


def test_index_route():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
