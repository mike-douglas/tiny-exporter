# sensor-exporter

This is a small Python flask API for exporting guage metrics. The API also can record metrics

## Running

```bash
flask run
```

## API

Exporting metrics:

```bash
curl "http://localhost:5000/metrics"
```

Posting metrics:

```bash
curl -X "POST" "http://localhost:5000/api/v1/metric/METRIC_NAME" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "value": 1234,
  "labels": {
    "sensor": "01234"
  }
}'
```
