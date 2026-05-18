# SLI / SLO Design (Assignment 2 + End Term)

## Service Level Indicators (SLIs)

| SLI | Definition | Measurement |
|-----|------------|-------------|
| Availability | Ratio of successful health checks | `up{job=...}` in Prometheus |
| Latency | Time to respond to HTTP requests | Proxy via request rate + app response (demo) |
| Error rate | Failed requests / total requests | `rate(*_errors_total) / rate(*_requests_total)` |
| Request success rate | HTTP 2xx responses / all responses | Order/Payment health and API responses |

## Service Level Objectives (SLOs)

| Objective | Target | Monitoring |
|-----------|--------|------------|
| Availability | ≥ 99% | Prometheus `up` metric per service |
| Latency | ≤ 200 ms (p95) | Load test + Grafana panels |
| Error rate | ≤ 1% | `OrderServiceHighErrorRate` alert threshold tuned to 5% demo; production target 1% |

## Error Budget

With 99% availability SLO, the monthly error budget is ~7.2 hours of downtime. Incident simulation (Order DB misconfiguration) consumes budget until detection and recovery complete.

## Alerting Mapping

- `ServiceDown` — availability breach
- `OrderServiceDBNotReady` — configuration-induced outage
- `OrderServiceHighErrorRate` — error rate SLO risk
