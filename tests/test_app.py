from fastapi.testclient import TestClient

from admin.app import app

client = TestClient(app)


def test_get_admin_home():
    """GET /admin returns an HTML response"""
    response = client.get('/')
    assert response.status_code == 200, 'Admin page did not return sucessfully'
    assert 'text/html' in response.headers['content-type'], 'Type is not HTML'
    assert 'text/html' in response.headers['content-type'], 'Type is not HTML'
