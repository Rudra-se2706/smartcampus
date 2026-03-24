import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    res = client.get('/')
    assert res.status_code == 200

def test_login_page(client):
    res = client.get('/login')
    assert res.status_code == 200

def test_register_page(client):
    res = client.get('/register')
    assert res.status_code == 200

def test_register_user(client):
    res = client.post('/api/register', data={
        'name': 'Test User',
        'email': 'test@test.com',
        'password': 'password123'
    })
    assert res.status_code in [200, 302]

def test_login_wrong_password(client):
    res = client.post('/api/login', data={
        'email': 'wrong@test.com',
        'password': 'wrongpass'
    })
    assert res.status_code in [200, 302]

def test_dashboard_redirect_if_not_logged_in(client):
    res = client.get('/dashboard')
    assert res.status_code == 302

def test_notices_redirect_if_not_logged_in(client):
    res = client.get('/notices')
    assert res.status_code == 302

def test_groups_redirect_if_not_logged_in(client):
    res = client.get('/groups')
    assert res.status_code == 302

def test_security_redirect_if_not_logged_in(client):
    res = client.get('/security')
    assert res.status_code == 302

def test_ai_redirect_if_not_logged_in(client):
    res = client.get('/ai')
    assert res.status_code == 302