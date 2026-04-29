# Assignment 4 Incident Response Report

## 1. Incident Summary

An outage was simulated in `order-service` by injecting an invalid database hostname through configuration (`BROKEN_DB_CONFIG=true`), causing API failures.

## 2. Impact Assessment

- Affected service: `order-service`
- User impact: order retrieval endpoint unavailable (`/orders`, `/health`)
- Other services remained healthy due to microservices isolation

## 3. Severity Classification

- Severity: **SEV-2**
- Rationale: Core business function degraded, no full platform outage

## 4. Timeline

- T0: Failure injected (wrong DB host)
- T0+2m: Monitoring showed order service errors
- T0+5m: Logs and health endpoint confirmed DB misconfiguration
- T0+8m: Configuration corrected and service restarted
- T0+10m: Service restored and metrics stabilized

## 5. Root Cause Analysis

The root cause was an invalid database host value in runtime configuration for `order-service`.

## 6. Mitigation Steps

1. Confirmed service failure via `/health` and Prometheus metrics.
2. Corrected config (`BROKEN_DB_CONFIG=false` / proper `DB_HOST`).
3. Restarted impacted container.

## 7. Resolution Confirmation

- `order-service` health endpoint returned HTTP 200.
- Prometheus target status returned to `UP`.
- User workflow for order retrieval resumed.
