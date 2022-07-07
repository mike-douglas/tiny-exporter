
from unicodedata import numeric

def labels_to_string(labels):
    return ','.join([
        '{}="{}"'.format(k, v) for k, v in labels.items()
    ])

class Metric(object):
    """A base class for a Metric storing ONE value"""
    def __init__(self, name: str, labels: list = [], help: str = '') -> None:
        self.name = name
        self.labels = labels

    def record_value(self, value: int, labels: list = []) -> None:
        self.value = value

    def export(self) -> str:
        return ('# HELP {name} {help}'
                '# TYPE {name} {type}'
                '{name}{{labels}} {value}').format(
                    name=self.name,
                    labels=labels_to_string(self.labels),
                    help=self.help,
                    value=self.value
                    )

    def __str__(self) -> str:
        return '{0}{1}'.format(self.name, self.labels)
