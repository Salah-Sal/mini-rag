# Monitoring & Metrics

This guide describes how **mini-rag** exposes runtime metrics, how to scrape them
with Prometheus and how to visualise them in Grafana.

---

## 1. What is Measured?

| Metric                          | Type      | Labels                         | Description                           |
| ------------------------------- | --------- | ------------------------------ | ------------------------------------- |
| `http_requests_total`           | Counter   | `method`, `endpoint`, `status` | Total number of HTTP requests handled |
| `http_request_duration_seconds` | Histogram | `method`, `endpoint`           | Latency (seconds) per HTTP request    |

Additional business-level metrics can be added in the future (e.g. number of
chunks indexed, tokens generated, LLM latency).

---

## 2. Application Exposure

The FastAPI app adds a Prometheus middleware in `src/utils/metrics.py` and
mounts a **private** endpoint:

```
GET /metrics
```

This endpoint is excluded from the OpenAPI schema and should be fire-walled in
production (see security considerations below).

---

## 3. Prometheus Configuration

Example scrape job (add to `docker/prometheus/prometheus.yml`):

```yaml
scrape_configs:
  - job_name: mini-rag-api
    metrics_path: /metrics
    scheme: http
    static_configs:
      - targets: ["mini-rag-api:5000"] # container name & port
```

If you used the provided `docker/docker-compose.yml`, add a service label or
static target so Prometheus can resolve the container.

---

## 4. Grafana Dashboard

1. Launch Grafana and add Prometheus as a data-source.
2. Import dashboard **ID 4701** ("Prometheus 2.0 Stats") as a quick starting
   point, or create a custom dashboard with panels:
   - Requests per second – query: `sum(rate(http_requests_total[1m]))`
   - 95th percentile latency – query:
     `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`

---

## 5. Alerts (Optional)

Define alert rules, e.g. high latency:

```yaml
- alert: HighRequestLatency
  expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 1
  for: 10m
  labels:
    severity: page
  annotations:
    summary: "95th percentile latency > 1s for 10m"
```

Connect Alertmanager to Slack / e-mail.

---

## 6. Security Considerations

- The `/metrics` endpoint is **unauthenticated**; restrict access via Nginx or
  a private network.
- Avoid exposing internal labels that might leak sensitive path information.

---

## 7. Extending Metrics

When you add new components, inject metrics where valuable:

```python
from prometheus_client import Gauge
INDEXED_CHUNKS = Gauge("rag_indexed_chunks_total", "Total chunks indexed")

#… after indexing batch
INDEXED_CHUNKS.inc(len(chunks))
```

Document any new metrics here.
