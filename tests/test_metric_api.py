import pytest
from api import app as flask_app

@pytest.fixture()
def app():
    app = flask_app
    app.config.update(dict(TESTING=True))

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_save_gauge_reading_label(client):
    response = client.post('/api/v2/metric/gauge/foo', json=dict(
        labels=dict(foo='bar'),
        value=100
    ))

    assert response.status_code == 200
    assert response.data == b'OK'

def test_save_gauge_reading_no_label(client):
    response = client.post('/api/v2/metric/gauge/foo', json=dict(
        labels=dict(),
        value=100
    ))

    assert response.status_code == 200
    assert response.data == b'OK'

def test_save_counter_reading_label(client):
    response = client.post('/api/v2/metric/counter/foo', json=dict(
        labels=dict(foo='bar'),
        value=100
    ))

    assert response.status_code == 200
    assert response.data == b'OK'

def test_save_counter_reading_nolabel(client):
    response = client.post('/api/v2/metric/counter/foo', json=dict(
        labels=dict(),
        value=100
    ))

    assert response.status_code == 200
    assert response.data == b'OK'

def test_save_histogram_reading_label(client):
    client.put('/api/v2/metric/histogram/foo', json=dict(
        buckets=[0.1, 0.2, 100, 200, 500]
    ))

    response = client.post('/api/v2/metric/histogram/foo', json=dict(
        labels=dict(foo='bar'),
        value=100
    ))

    assert response.status_code == 200
    assert response.data == b'OK'

def test_save_histogram_reading_nolabel(client):
    response = client.post('/api/v2/metric/histogram/foo', json=dict(
        labels=dict(),
        value=100
    ))

    assert response.status_code == 200
    assert response.data == b'OK'

