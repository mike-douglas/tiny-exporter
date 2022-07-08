import pytest  # noqa: F401


def test_save_gauge_reading_label(client):
    response = client.post('/api/v2/metric/gauge/foo', json=dict(
        labels=dict(foo='bar'),
        value=100
    ))

    assert response.status_code == 200


def test_save_gauge_reading_no_label(client):
    response = client.post('/api/v2/metric/gauge/foo', json=dict(
        value=100
    ))

    assert response.status_code == 200


def test_save_counter_reading_label(client):
    response = client.post('/api/v2/metric/counter/foo', json=dict(
        labels=dict(foo='bar'),
        value=100
    ))

    assert response.status_code == 200


def test_save_counter_reading_nolabel(client):
    response = client.post('/api/v2/metric/counter/foo', json=dict(
        value=100
    ))

    assert response.status_code == 200


def test_save_histogram_reading_label(client):
    client.put('/api/v2/metric/histogram/foo', json=dict(
        buckets=[0.1, 0.2, 100, 200, 500]
    ))

    response = client.post('/api/v2/metric/histogram/foo', json=dict(
        labels=dict(foo='bar'),
        value=100
    ))

    assert response.status_code == 200


def test_save_histogram_reading_nolabel(client):
    response = client.post('/api/v2/metric/histogram/foo', json=dict(
        value=100
    ))

    assert response.status_code == 200


def test_configure_gauge_help_text(client):
    response = client.put('/api/v2/metric/gauge/temp', json=dict(
        help='Temperature'
    ))

    assert response.status_code == 201


def test_configure_gauge_labels(client):
    response = client.put('/api/v2/metric/gauge/temp', json=dict(
        labels=dict(room='office')
    ))

    assert response.status_code == 201


def test_configure_histogram_buckets(client):
    response = client.put('/api/v2/metric/histogram/delivery_time', json=dict(
        buckets=[120, 600, 1200, 2400, '+Inf']
    ))

    assert response.status_code == 201

