from collections import defaultdict
from flask import Flask, request

app = Flask(__name__)
app.logger.setLevel('INFO')

# Default labels for this exporter
labels = {
}

data = defaultdict(lambda: dict())

# Data storage
gauges = defaultdict(lambda: dict())
counters = defaultdict(lambda: defaultdict(lambda: 0))

histogram_bucket = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: 0)))
histogram_sum = defaultdict(lambda: defaultdict(lambda: 0))
histogram_count = defaultdict(lambda: defaultdict(lambda: 0))
histogram_def = dict()


def labels_to_string(labels):
    return ','.join([
        '{}="{}"'.format(k, v) for k, v in labels.items()
    ])


@app.route('/metrics')
def metrics():
    '''Export metrics for Prometheus'''
    output = []

    for metric, labels in gauges.items():
        output.append('# HELP {0} {0}'.format(metric))
        output.append('# TYPE {0} gauge'.format(metric))

        for label, value in labels.items():
            output.append('{metric}{{{label}}} {value}'.format(
                metric=metric,
                label=label,
                value=value
            ))

    for metric, labels in counters.items():
        output.append('# HELP {0} {0}'.format(metric))
        output.append('# TYPE {0} counter'.format(metric))

        for label, value in labels.items():
            output.append('{metric}{{{label}}} {value}'.format(
                metric=metric,
                label=label,
                value=value
            ))

    for metric, labels in histogram_bucket.items():
        output.append('# HELP {0} {0}'.format(metric))
        output.append('# TYPE {0} histogram'.format(metric))

        for label, bucket in labels.items():
            for bucket_label, value in bucket.items():
                output.append('{metric}_bucket{{{label},{bucket}}} {value}'.format(
                    metric=metric, label=label, bucket=bucket_label, value=value))

            output.append('{metric}_sum{{{label}}} {value}'.format(
                metric=metric,
                label=label,
                value=histogram_sum[metric][label]
            ))

            output.append('{metric}_count{{{label}}} {value}'.format(
                metric=metric,
                label=label,
                value=histogram_count[metric][label]
            ))

    return '\n'.join(output)


@app.route('/api/v1/metric/<metric>', methods=['POST'])
@app.route('/api/v2/metric/gauge/<metric>', methods=['POST'])
def save_gauge_reading(metric):
    '''Record a value for a gauge metric with provided labels'''
    all_labels = request.json.get('labels', dict())
    all_labels.update(labels)

    label = labels_to_string(all_labels)
    value = request.json.get('value')

    gauges[metric][label] = value

    app.logger.info(request.json)

    return 'OK'


@app.route('/api/v2/metric/counter/<metric>', methods=['POST'])
def save_counter_reading(metric):
    '''Increment a counter metric with provided labels'''
    all_labels = request.json.get('labels', dict())
    all_labels.update(labels)

    label = labels_to_string(all_labels)

    counters[metric][label] += 1

    app.logger.info(request.json)

    return 'OK'


@app.route('/api/v2/metric/histogram/<metric>', methods=['POST'])
def save_histogram_reading(metric):
    '''Increment a historgram bucket given a value with provided labels'''
    all_labels = request.json.get('labels', dict())
    all_labels.update(labels)

    value = request.json.get('value')

    if metric in histogram_def.keys():
        label = labels_to_string(all_labels)
        histogram_count[metric][label] += 1
        histogram_sum[metric][label] += value

        for bucket in histogram_def[metric]:
            bucket_label = labels_to_string(dict(le=str(bucket)))

            histogram_bucket[metric][label][bucket_label]

            if bucket == '+Inf' or value <= bucket:
                histogram_bucket[metric][label][bucket_label] += 1

    else:
        return 'Error: buckets for metric {} have not been set'.format(metric)

    return 'OK'


@app.route('/api/v2/metric/histogram/<metric>', methods=['PUT'])
def create_or_update_histogram(metric):
    '''Set the buckets for a histogram metric'''
    buckets = request.json.get('buckets')

    histogram_def[metric] = buckets

    return 'OK'
