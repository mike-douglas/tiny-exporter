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


def test_gauge_export(client):
    response = client.post('/api/v2/metric/gauge/foo', json=dict(
        labels=dict(foo='bar'),
        value=100
    ))

    response = client.get('/metrics')
    assert '''
# HELP foo foo
# TYPE foo gauge
foo{foo="bar"} 100
'''.strip() in str(response.data, encoding='UTF8')


def test_counter_export(client):
    response = client.post('/api/v2/metric/counter/foo', json=dict(
        labels=dict(foo='bar')
    ))

    response = client.get('/metrics')
    assert '''
# HELP foo foo
# TYPE foo counter
foo{foo="bar"} 1
'''.strip() in str(response.data, encoding='UTF8')

    response = client.post('/api/v2/metric/counter/foo', json=dict(
        labels=dict(foo='bar')
    ))

    response = client.get('/metrics')
    assert '''
# HELP foo foo
# TYPE foo counter
foo{foo="bar"} 2
'''.strip() in str(response.data, encoding='UTF8')


def test_histogram_export(client):
    client.put('/api/v2/metric/histogram/foo', json=dict(
        buckets=[1, 2, 300, '+Inf']
    ))
    client.post('/api/v2/metric/histogram/foo', json=dict(
        labels=dict(foo='bar'),
        value=100
    ))

    response = client.get('/metrics')
    print(response.data)
    assert '''
# HELP foo foo
# TYPE foo histogram
foo_bucket{foo="bar",le="1"} 0
foo_bucket{foo="bar",le="2"} 0
foo_bucket{foo="bar",le="300"} 1
foo_bucket{foo="bar",le="+Inf"} 1
'''.strip() in str(response.data, encoding='UTF8')
