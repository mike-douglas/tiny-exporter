# tiny-exporter

[![Release](https://img.shields.io/github/release/mike-douglas/tiny-exporter.svg?style=flat-square)](https://github.com/mike-douglas/tiny-exporter/releases/latest)
![All Tests](https://github.com/mike-douglas/tiny-exporter/actions/workflows/run_tests.yml/badge.svg?branch=main)
[![GitHub issues](https://img.shields.io/github/issues/mike-douglas/tiny-exporter)](https://github.com/mike-douglas/tiny-exporter/issues)
[![GitHub license](https://img.shields.io/github/license/mike-douglas/tiny-exporter)](https://github.com/mike-douglas/tiny-exporter/blob/main/LICENSE.txt)

Tiny exporter is a lightweight RESTful API for collecting metrics that can be exported to [Prometheus][].

It supports storing [gauge][], [counter][], and [histogram][] metrics with labels.

## Example Uses

* A metrics collection and export agent for IoT devices
* A sidecar to an app that wants to collect metrics
* A lightweight metrics agent and exporter for a k8s cluster

## Running

The easiest way to use this is with the Docker image at [mdouglas/tiny-exporter][].

### Running with Docker

```bash
docker run -d -p 5000:9800 mdouglas/tiny-exporter:latest
```

### Local Development / Running Manually

For local development or to run it yourself, it's simply a [Flask][] app. Run it with:

```bash
FLASK_APP=api flask run
```

## Documentation

Documentation can be found at the [wiki](https://github.com/mike-douglas/tiny-exporter/wiki).

## License

See [LICENSE][]

[gauge]: https://prometheus.io/docs/concepts/metric_types/#gauge
[counter]: https://prometheus.io/docs/concepts/metric_types/#counter
[histogram]: https://prometheus.io/docs/concepts/metric_types/#histogram
[Flask]: https://flask.palletsprojects.com
[mdouglas/tiny-exporter]: https://hub.docker.com/r/mdouglas/tiny-exporter
[Prometheus]: https://prometheus.io/
[LICENSE]: https://github.com/mike-douglas/tiny-exporter/blob/main/LICENSE.txt
