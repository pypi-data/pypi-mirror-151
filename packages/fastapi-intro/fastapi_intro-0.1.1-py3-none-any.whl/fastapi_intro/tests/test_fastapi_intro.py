""" 
Description: Testing file
Author: Prabal Pathak
"""
from fastapi.testclient import TestClient
from fastapi_intro import __version__
from main import app

client = TestClient(app)


def test_version():
    """Test application version"""
    assert __version__ == "0.1.0"


def test_root():
    """
    Test root application url
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
