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
- 9090 (Prometheus)

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
