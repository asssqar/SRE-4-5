# End Term Project Report

## Comprehensive SRE Implementation for a Distributed Microservices System

**Git repository:** https://github.com/asssqar/SRE-4-5.git

---

## 1. Title

End-to-End Implementation of Site Reliability Engineering Practices in a Multi-Orchestrated Microservices Infrastructure Using Docker Swarm, Kubernetes, Terraform, and Ansible

## 2. Abstract

This project implements SRE principles on a distributed microservices platform: six FastAPI services behind an Nginx frontend, PostgreSQL, Redis, Prometheus, and Grafana. The stack runs under Docker Compose locally, Docker Swarm for replicated clustering, and Kubernetes for declarative deployments with HPA. Terraform provisions AWS EC2; Ansible automates VM setup and deployment. A simulated Order Service database misconfiguration demonstrates incident detection, mitigation, and postmortem analysis.

## 3. Objectives (Completed)

1. Six microservices: Auth, Product, Order, Payment, Notification, User Profile
2. Multi-orchestration: Docker Compose, Docker Swarm (`docker-stack.yml`), Kubernetes (`k8s/`)
3. Terraform infrastructure (`terraform/`)
4. Ansible automation (`ansible/`)
5. SLIs and SLOs (`reports/sli_slo.md`)
6. Prometheus + Grafana monitoring (`monitoring/`)
7. Incident simulation (`BROKEN_DB_CONFIG`, Assignment 4)
8. Postmortem (`reports/postmortem.md`)
9. Automation and capacity planning (`reports/assignment6_automation_capacity_report.md`)

## 4. System Architecture

```
User → Frontend (Nginx) → API routes → Microservices (6)
                              ↓
                    PostgreSQL + Redis
Monitoring: Prometheus → Grafana
IaC: Terraform → EC2 VM
Config: Ansible → Docker + Compose deploy
Orchestration: Compose | Swarm | Kubernetes
```

## 5. Microservices

| Service | Port | Responsibility |
|---------|------|----------------|
| Auth | 8001 | Login / JWT simulation |
| Product | 8002 | Product catalog |
| Order | 8003 | Orders (PostgreSQL-dependent) |
| User Profile | 8004 | User data |
| Notification | 8005 | Email/alert simulation |
| Payment | 8006 | Payment simulation |

## 6. Multi-Orchestration

### Docker Swarm

```bash
docker swarm init
docker compose build
docker stack deploy -c docker-stack.yml sre
```

### Kubernetes

```bash
docker compose build
# Tag images as sre-*-service:latest (see DEPLOYMENT.md)
kubectl apply -f k8s/
```

## 7. Terraform

Reproducible EC2 + security group (SSH, HTTP, Grafana, Prometheus). See `reports/assignment5_terraform_report.md`.

## 8. Ansible

```bash
# Edit ansible/inventory/hosts.ini with VM IP
ansible-playbook ansible/playbooks/site.yml
```

Roles: common (packages), docker (engine), app (sync + compose up), monitoring (health checks).

## 9. Monitoring

- Metrics: CPU (process), request counters, error counters, `order_service_db_ready`
- Dashboard: `monitoring/grafana/dashboards/microservices-overview.json`
- Alerts: `monitoring/alerts.yml`

## 10. Incident Simulation

Order Service fails when `BROKEN_DB_CONFIG=true`. Detected via health endpoint, Prometheus alerts, and Grafana. Recovery: set `false`, restart service. See `reports/assignment4_incident_report.md` and `reports/postmortem.md`.

## 11. Capacity Planning

Order and Payment services are primary scaling candidates; PostgreSQL is the data bottleneck. Strategies: HPA on order-service (K8s), Swarm/Compose replicas, vertical VM scaling via Terraform variables.

## 12. Deliverables Checklist

- [x] Microservices source code (6 services)
- [x] Docker Compose + Swarm (`docker-compose.yml`, `docker-stack.yml`)
- [x] Kubernetes manifests (`k8s/`)
- [x] Terraform (`terraform/`)
- [x] Ansible playbooks (`ansible/`)
- [x] Monitoring setup
- [x] Incident report and postmortem
- [ ] Screenshots (capture locally for PDF)
- [ ] **Submit PDF with Git link only** — use this report + screenshots

## 13. How to Run Demo

```powershell
docker compose up --build -d
# Frontend: http://localhost
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9091
```

## 14. Conclusion

The project demonstrates the full SRE lifecycle: design, multi-platform deployment, observability, incident response, infrastructure automation, and scalability planning—integrated into a single reproducible repository.

---

**Repository for submission:** https://github.com/asssqar/SRE-4-5.git
