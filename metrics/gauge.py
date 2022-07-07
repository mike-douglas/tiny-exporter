from collections import defaultdict

from metrics import Metric, MetricType, labels_to_string

class GaugeMetric(Metric):
    def __init__(self, name: str, labels: list = [], help: str = '') -> None:
        super.__init__(self, name, labels, help)

        self.type = MetricType.Gauge
        self.values = defaultdict(lambda: 0)
    
    def record_value(self, value: int, labels: list = []) -> None:
        self.values[labels_to_string(labels + self.labels)] = value