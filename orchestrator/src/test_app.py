import pytest
from orchestrator.src.app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_checkout_post(client):
    response = client.post('/checkout', json={
        "user": {"name": "Test User", "items": ["Book 1"]},
        "orderId": "12345"
    })
    assert response.status_code == 200
    assert 'status' in response.json
