from collections import defaultdict
from flask import Flask, request

app = Flask(__name__)

labels = {
    'host': 'raspberry-pi'
}

data = defaultdict(lambda: dict())

def labels_to_string(l):
    return ','.join([
        '{}="{}"'.format(k, v) for k, v in l.items()
    ])

@app.route('/metrics')
def metrics():
    output = []

    for metric, labels in data.items():
        output.append('# HELP {0} {0}'.format(metric))
        output.append('# TYPE {0} guage'.format(metric))

        for label, value in labels.items():
            output.append('{metric}{{{label}}} {value}'.format(
                metric=metric,
                label=label,
                value=value
            ))

    return '\n'.join(output)

@app.route('/api/v1/metric/<metric>', methods=['POST'])
def save_reading(metric):
    all_labels = request.json.get('labels', dict())
    all_labels.update(labels)

    label = labels_to_string(all_labels)

    data[metric][label] = request.json.get('value')

    return 'OK'