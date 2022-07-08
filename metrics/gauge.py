from collections import defaultdict

from metrics import Metric, MetricType, labels_to_string


class GaugeMetric(Metric):
    def __init__(self, name: str, labels: dict = {}, help: str = '') -> None:
        Metric.__init__(self, name, labels, help)

        self.type = MetricType.Gauge
        self.values = defaultdict(lambda: 0)

    def record_value(self, value: int, labels: dict = {}) -> None:
        labels_copy = self.labels.copy()
        labels_copy.update(labels)

        self.values[labels_to_string(labels_copy)] = value

    def export(self) -> str:
        exported_lines = list()

        for labels, value in self.values.items():
            exported_lines.append(
                '{name}{{{labels}}} {value}'.format(
                    name=self.name,
                    labels=labels,
                    value=value
                )
            )

        return '\n'.join(exported_lines)
