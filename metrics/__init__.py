
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

    def __init__(self, name: str, labels: dict = {}, help: str = '') -> None:
        self.name = name
        self.labels = labels
        self.type = MetricType.Unknown
        self.help = help

    def record_value(self, value: int, labels: dict = {}) -> None:
        self.value = value

    def export_header(self) -> str:
        exported_lines = list()

        if len(self.help) == 0:
            exported_lines.append('# HELP {}'.format(self.name))
        else:
            exported_lines.append('# HELP {} {}'.format(
                self.name,
                self.help
            ))

        exported_lines.append('# TYPE {} {}'.format(
            self.name,
            self.type
        ))

        return '\n'.join(exported_lines)

    def export(self) -> str:
        return '{name}{{{labels}}} {value}'.format(
            name=self.name,
            value=self.value,
            labels=labels_to_string(self.labels)
        )

    def __str__(self) -> str:
        return '{0}{1}'.format(self.name, labels_to_string(self.labels))
