from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_mobile_access_endpoint() -> None:
    response = client.get('/api/system/mobile-access')
    assert response.status_code == 200
    body = response.json()
    assert 'run_command' in body
    assert body['mobile_url_pattern'].startswith('http://')
