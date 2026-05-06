# Assignment 4-5 Final Submission

## 1. Project Overview

Implemented a containerized microservices platform with:
- Frontend via Nginx
- FastAPI services: auth, product, order, user, chat
- PostgreSQL
- Prometheus + Grafana
- Terraform for VM provisioning

## 2. Infrastructure as Code (Assignment 5)

Terraform files:
- `terraform/main.tf`
- `terraform/variables.tf`
- `terraform/outputs.tf`
- `terraform/terraform.tfvars`

Ports opened by security group:
- 22 (SSH)
- 80 (HTTP)
- 3000 (Grafana)
- 9091 (Prometheus)

### Evidence
- Screenshot A: `terraform init` success
- Screenshot B: `terraform plan` output
- Screenshot C: `terraform apply` output with created resources
- Screenshot D: output showing `instance_public_ip`

## 3. Container Deployment

Deployment uses `docker-compose.yml` with isolated containers and internal networking.

### Evidence
- Screenshot E: `docker compose ps` (all containers running)
- Screenshot F: frontend page on `http://localhost`
- Screenshot G: Prometheus targets page (`UP`)
- Screenshot H: Grafana dashboard with service metrics

## 4. Incident Response Simulation (Assignment 4)

### Simulated Incident
Order service database misconfiguration introduced using:
- `BROKEN_DB_CONFIG=true`

### Detection
- HTTP 500 on `order-service /health`
- Errors visible in Prometheus/Grafana

### Analysis
- Container health checks and endpoint responses
- Root cause identified as invalid DB hostname from runtime config

### Mitigation
1. Set `BROKEN_DB_CONFIG=false`
2. Rebuild/restart `order-service`
3. Validate metrics and endpoint recovery

### Restoration
- `/health` returns 200
- Prometheus target and metrics normalized

### Evidence
- Screenshot I: Failure state (HTTP 500)
- Screenshot J: Monitoring evidence during incident
- Screenshot K: Service restored (HTTP 200)
- Screenshot L: Post-incident stable dashboard

## 5. Incident Report and Postmortem

Documents:
- `reports/assignment4_incident_report.md`
- `reports/postmortem.md`
- `reports/assignment5_terraform_report.md`

Postmortem action items:
1. Startup DB validation checks
2. Alerting for error spikes
3. Pre-deploy configuration validation
4. Improved runbook automation

## 6. Conclusion

The implementation demonstrates reproducible infrastructure provisioning, containerized service deployment, observability integration, and structured incident response with documented recovery and preventive actions.

---

# Assignment 6: Automation + Capacity Planning Submission

## 1. Automation (SRE)

Implemented automation mechanisms to reduce manual operations and improve reliability:
- Docker Compose provides consistent multi-container deployment (`docker compose up -d`)
- Self-healing via `restart: unless-stopped` for services
- Health endpoints (`/health`) for each microservice
- Docker healthchecks for early failure detection and recovery workflows
- Configuration validation through documented required environment variables (see `DEPLOYMENT.md`)

## 2. Monitoring + Alerting

Prometheus configuration:
- Scrapes each service `/metrics`
- Loads alert rules from `monitoring/alerts.yml`

Implemented alert rules:
- Service down (`ServiceDown`)
- Order DB misconfiguration (`OrderServiceDBNotReady`)
- High Order error ratio (`OrderServiceHighErrorRate`)
- High Order CPU (process CPU metric) (`OrderServiceHighCPU`)

## 3. Capacity Planning

Load simulation:
- Execute concurrent requests to the Order API and observe metrics (CPU, request rate, errors)

Observations and bottlenecks:
- Order Service is the primary candidate for saturation under load
- Database can become a bottleneck if connections/queries scale poorly

Scaling strategies:
- Horizontal scaling: replicate Order Service instances behind a load balancer
- Vertical scaling: increase VM/container CPU and memory allocations
- Database optimization: pooling, tuning, query optimization

## 4. Evidence Required (Screenshots)

- Screenshot M: Prometheus targets all `UP`
- Screenshot N: Prometheus Alerts page showing loaded rules
- Screenshot O: Grafana dashboard during load test
- Screenshot P: Order service failure (BROKEN_DB_CONFIG=true) and alert firing
- Screenshot Q: Service recovery after mitigation (BROKEN_DB_CONFIG=false)
