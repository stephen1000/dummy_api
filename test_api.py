"""Sends a few test cases at the (running) API:
- no authentication
- bad authentication
- good authentication
"""
import pytest
import requests

from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def json_headers():
    return {"Accept": "application/json"}


def test_no_auth(client, json_headers):
    """ Test that an empty apikey raises a 401 """
    response = client.post("/", headers=json_headers)
    assert response.status_code == 401


def test_bad_auth(client, json_headers):
    """ Test that a bad apikey raises a 401 """
    json_headers["X-API-KEY"] = "foo bar"
    response = client.post("/", headers=json_headers)
    assert response.status_code == 401


def test_good_auth(client, json_headers):
    """ Test that a good apikey succeeds """
    json_headers["X-API-KEY"] = "12345"
    response = client.post("/", headers=json_headers)
    assert response.status_code == 200
