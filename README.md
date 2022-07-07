# tiny-exporter

Tiny exporter is a lightweight RESTful API for collecting metrics that can be exported to [Prometheus][].

It supports storing [gauge][], [counter][], and [histogram][] metrics with labels.

## Example Uses

* A metrics collection and export agent for IoT devices
* A sidecar to an app that wants to collect metrics
* A lightweight metrics agent and exporter for a k8s cluster

## Running

The easiest way to use this is with the Docker image at [mdouglas/tiny-exporter][].

For local development or to run it yourself, it's simply a [Flask][] app. Run it with:

```bash
flask run
```

## Documentation

Documentation coming soon.

## License

See [LICENSE](LICENSE.txt)

[gauge]: https://prometheus.io/docs/concepts/metric_types/#gauge
[counter]: https://prometheus.io/docs/concepts/metric_types/#counter
[histogram]: https://prometheus.io/docs/concepts/metric_types/#histogram
[Flask]: https://flask.palletsprojects.com
[mdouglas/tiny-exporter]: https://hub.docker.com/mdouglas/tiny-exporter
[Prometheus]: https://prometheus.io/