from collections import defaultdict
from metrics import Metric, MetricType, labels_to_string


class HistogramMetric(Metric):
    DefaultBuckets: list = [0.1, 0.2, 0.4, 1, 3, 8, 20, 60, 120]

    def __init__(self, name: str, buckets: list = DefaultBuckets,
                 labels: dict = {}, help: str = '') -> None:
        Metric.__init__(self, name, labels, help)

        self.type = MetricType.Histogram
        self.buckets = buckets
        self.values = defaultdict(lambda: defaultdict(lambda: 0))
        self.sums = defaultdict(lambda: 0)
        self.counts = defaultdict(lambda: 0)

    def record_value(self, value: float, labels: dict = {}) -> None:
        labels_copy = self.labels.copy()
        labels_copy.update(labels)

        labels_string = labels_to_string(labels_copy)

        for bucket in self.buckets:
            bucket_label_string = labels_to_string(dict(le=str(bucket)))

            self.values[labels_string][bucket_label_string]

            if bucket == '+Inf' or value <= bucket:
                self.values[labels_string][bucket_label_string] += 1

        self.sums[labels_string] += value
        self.counts[labels_string] += 1

    def export(self) -> str:
        exported_lines = list()

        for labels, buckets in self.values.items():
            for bucket, value in buckets.items():
                exported_lines.append(
                    '{name}_bucket{{{labels},{bucket}}} {value}'.format(
                        name=self.name,
                        labels=labels,
                        value=value,
                        bucket=bucket
                    )
                )

            exported_lines.append(
                '{name}_sum{{{labels}}} {value}'.format(
                    name=self.name,
                    labels=labels,
                    value=self.sums[labels]
                )
            )

            exported_lines.append(
                '{name}_count{{{labels}}} {value}'.format(
                    name=self.name,
                    labels=labels,
                    value=self.counts[labels]
                )
            )

        return '\n'.join(exported_lines)
