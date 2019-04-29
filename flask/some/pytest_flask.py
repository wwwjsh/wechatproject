import os
import pytest

from manager import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()


    yield client
#
#
# def test_empty_db(client):
#     """Start with a blank database."""
#
#     rv = client.get('/')
#     print(rv.data)
#     assert b'No entries here so far' in rv.data

def setup_module(module):
    app.testing = True


@pytest.fixture
def test_empty_db(client):
    rv = client.get('/')
    print(rv.data)
    assert b'No entries here so far' in rv.data