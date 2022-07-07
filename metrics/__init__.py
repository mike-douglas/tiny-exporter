
from unicodedata import numeric

def labels_to_string(labels: list) -> str:
    return ','.join([
        '{}="{}"'.format(k, v) for k, v in labels.items()
    ])

class MetricType(object):
    Histogram = 'histogram'
    Gauge = 'gauge'
    Counter = 'counter'
    Unknown = 'unknown'

class Metric(object):
    """A base class for a Metric storing ONE value"""
    def __init__(self, name: str, labels: list = [], help: str = '') -> None:
        self.name = name
        self.labels = labels
        self.type = MetricType.Unknown

    def record_value(self, value: int, labels: list = []) -> None:
        self.value = value

    def export_header(self) -> str:
        return ('# HELP {name} {help}',
                '# TYPE {name} {type}').format(
                    **self.__dict__
                )

    def export(self) -> str:
        return '{name}{{labels}} {value}'.format(
                    name=self.name,
                    value=self.value,
                    labels=labels_to_string(self.labels)
                    )

    def __str__(self) -> str:
        return '{0}{1}'.format(self.name, labels_to_string(self.labels))
