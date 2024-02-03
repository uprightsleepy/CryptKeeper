from unittest.mock import patch

import pytest
from flask import Flask

from app.routes.encryption_routes import encryption_blueprint


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(encryption_blueprint)
    with app.test_client() as client:
        yield client


def test_encrypt_route_success(client):
    with patch('app.services.encryption_service.encrypt') as mock_encrypt:
        mock_encrypt.return_value = {'encrypted_data': 'encrypted_text'}
        response = client.post('/encrypt', json={
            'id': 'test_id',
            'itemType': 'test_type',
            'plaintext': 'test_text'
        })
        assert response.status_code == 200


def test_encrypt_route_validation_error(client):
    response = client.post('/encrypt', json={})
    assert response.status_code == 400
    assert 'id' in response.json
    assert 'itemType' in response.json


def test_decrypt_route_success(client):
    with patch('app.services.encryption_service.decrypt') as mock_encrypt:
        mock_encrypt.return_value = {'decrypted_data': 'test_text'}
        response = client.post('/decrypt', json={
            'id': 'test_id',
            'itemType': 'test_type'
        })
        assert response.status_code == 200


def test_decrypt_route_validation_error(client):
    response = client.post('/decrypt', json={})
    assert response.status_code == 400
    assert 'id' in response.json
    assert 'itemType' in response.json


