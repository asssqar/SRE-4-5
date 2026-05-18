# Assignment 6 Report

## Title
Automation and Capacity Planning in a Containerized Microservices System Following Incident Response and Infrastructure Provisioning

## Objectives

This assignment extends Assignments 4 (incident response) and 5 (Terraform IaC) by:
- Introducing automation mechanisms to reduce manual intervention
- Adding monitoring-based alerting
- Performing basic capacity planning through load simulation and metric analysis
- Proposing scaling strategies for increased demand

## System Context

The system is a Dockerized microservices architecture consisting of:
- Frontend (Nginx reverse proxy + single control panel page)
- Backend services (FastAPI): auth, product, order, user, notification, payment
- PostgreSQL database
- Monitoring stack: Prometheus + Grafana
- IaC: Terraform (AWS EC2 + security group)

## Automation in SRE

### 1) Automated Deployment

Deployment is standardized through `docker-compose.yml`:
- One command to build and run the entire stack: `docker compose up -d --build`
- Isolated service networking via a dedicated Compose network
- Standardized environment configuration (via Compose env defaults and `.env` if used)

### 2) Health Checks and Self-Healing

Each microservice provides:
- `GET /health` endpoint (service liveness + basic readiness)
- `GET /metrics` endpoint for Prometheus scraping

Docker Compose adds:
- `restart: unless-stopped` to automatically recover from crashes
- `healthcheck` probes hitting each service `/health`

### 3) Monitoring-Based Alerting

Prometheus:
- Scrapes each service’s `/metrics`
- Loads alert rules from `monitoring/alerts.yml`

Implemented alert rules include:
- `ServiceDown`: Prometheus cannot scrape a service
- `OrderServiceDBNotReady`: misconfiguration simulation via `BROKEN_DB_CONFIG=true`
- `OrderServiceHighErrorRate`: elevated error ratio based on counters
- `OrderServiceHighCPU`: high CPU usage for Order process (via `process_cpu_seconds_total`)

### 4) Log-Based Troubleshooting (Operational Practice)

Troubleshooting uses:
- `docker compose logs <service>` for rapid diagnosis
- Prometheus/Grafana to correlate symptoms (errors, downtime) with the affected service

### 5) Configuration Validation

To prevent incidents caused by configuration errors:
- Required variables are documented in `DEPLOYMENT.md`
- The Order Service simulates misconfiguration using `BROKEN_DB_CONFIG` to demonstrate detection and recovery

## Capacity Planning

### Metrics Collected

Using Prometheus and Grafana:
- Request rate (RPS) via counters (e.g. `rate(order_requests_total[1m])`)
- Error rate via counters (e.g. `rate(order_errors_total[1m])`)
- Process CPU usage via default Prometheus Python process metric (e.g. `rate(process_cpu_seconds_total{job="order-service"}[2m])`)

### Load Simulation

Example load methods (documented in `DEPLOYMENT.md`):
- `hey` to run concurrent requests against the Order API
- A simple PowerShell request loop for basic stress

### Observations (Expected)

Under increased load:
- Order Service CPU usage rises and becomes the first pressure point
- Response latency can rise (observed via client and indirectly via increased error ratio)
- The database may become a bottleneck if throughput or connection handling is insufficient

### Scaling Strategies

1) Horizontal scaling:
- Run multiple instances of Order Service and distribute traffic (load balancer / reverse proxy)

2) Vertical scaling:
- Increase VM resources in Terraform (instance type)
- Increase container CPU/memory limits (if enforced) depending on target platform

3) Database optimization:
- Connection pooling
- Query tuning and indexing
- Allocating adequate disk and memory resources

## Improvements Based on Assignments 4 and 5

From the incident (Assignment 4):
- Added proactive detection via healthchecks and alerting
- Reduced recovery time through restart policies and faster localization via metrics

From IaC (Assignment 5):
- Reproducible infrastructure provisioning with Terraform
- Clear documentation for deployment and validation steps

## Supporting Evidence Checklist (Screenshots)

Include screenshots showing:
- Running containers (`docker compose ps`)
- Prometheus targets are `UP`
- Prometheus Alerts page showing loaded rules
- Grafana dashboard panels under load
- Incident simulation (`BROKEN_DB_CONFIG=true`) and recovery (`false`)

