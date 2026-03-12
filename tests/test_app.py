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


def test_project_manifest_endpoint() -> None:
    response = client.get('/api/project/manifest')
    assert response.status_code == 200
    body = response.json()
    assert 'app' in body
    assert 'tests' in body
    assert any(p.endswith('app/main.py') for p in body['app'])
