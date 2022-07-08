from flask import Flask, Blueprint, request, current_app

from metrics import MetricType, gauge, histogram, counter

exporter = Blueprint('exporter', __name__)
v1_api = Blueprint('v1_api', __name__)
v2_api = Blueprint('v2_api', __name__)


def create_app() -> Flask:
    app = Flask(__name__)

    app.logger.setLevel('INFO')

    app.register_blueprint(exporter)
    app.register_blueprint(v2_api, url_prefix='/api/v2')
    app.register_blueprint(v1_api, url_prefix='/api/v1')

    with app.app_context():
        current_app.gauges = dict()
        current_app.counters = dict()
        current_app.histograms = dict()

    return app


supported_metrics = [
    MetricType.Counter,
    MetricType.Histogram,
    MetricType.Gauge
]


@exporter.route('/metrics')
def metrics():
    '''Export metrics for Prometheus'''
    output = []

    for group in [current_app.gauges.values(), current_app.counters.values(),
                  current_app.histograms.values()]:
        for metric in group:
            output.append(metric.export_header())
            output.append(metric.export())

    return '\n'.join(output)


@v1_api.route('/metric/<metric>', methods=['POST'])
def save_gauge_metric(metric):
    return save_reading(MetricType.Gauge, metric)


@v2_api.route('/metric/<metric_type>/<metric>', methods=['POST'])
def save_reading(metric_type, metric):
    '''Save a reading for a metric'''
    labels = request.json.get('labels', dict())
    value = request.json.get('value')

    if metric_type == MetricType.Counter:
        if metric not in current_app.counters:
            current_app.counters[metric] = counter.CounterMetric(metric)

        current_app.counters[metric].record_value(labels=labels)
    elif metric_type == MetricType.Gauge:
        if metric not in current_app.gauges:
            current_app.gauges[metric] = gauge.GaugeMetric(metric)

        current_app.gauges[metric].record_value(value, labels=labels)
    elif metric_type == MetricType.Histogram:
        if metric not in current_app.histograms:
            current_app.histograms[metric] = histogram.HistogramMetric(metric)

        current_app.histograms[metric].record_value(value, labels=labels)
    else:
        return 'Unsupported metric type (valid types are: {})'.format(
            ', '.join(supported_metrics)), 400

    return 'OK'


@v2_api.route('/metric/<metric_type>/<metric>', methods=['PUT'])
def create_or_replace(metric_type, metric):
    '''Resets the data in a metric and recreates it'''
    labels = request.json.get('labels', dict())
    help = request.json.get('help', '')

    if metric_type == MetricType.Counter:
        current_app.counters[metric] = counter.CounterMetric(
            metric,
            labels=labels,
            help=help
        )
    elif metric_type == MetricType.Gauge:
        current_app.gauges[metric] = gauge.GaugeMetric(
            metric,
            labels=labels,
            help=help
        )
    elif metric_type == MetricType.Histogram:
        buckets = request.json.get('buckets', [])
        current_app.histograms[metric] = histogram.HistogramMetric(
            metric,
            buckets=buckets,
            labels=labels,
            help=help
        )
    else:
        'Unsupported metric type (valid types are: {})'.format(
            ', '.join(supported_metrics)), 400

    return 'OK'
