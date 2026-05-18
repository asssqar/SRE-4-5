# SRE End Term Project — Distributed Microservices

Full **Site Reliability Engineering** implementation: 6 microservices, Docker Compose / Swarm / Kubernetes, Terraform, Ansible, Prometheus + Grafana, incident simulation.

**Repository:** https://github.com/asssqar/SRE-4-5.git

## Project Structure

| Path | Description |
|------|-------------|
| `services/` | Auth, Product, Order, Payment, Notification, User Profile (FastAPI) |
| `frontend/` | Nginx control panel |
| `docker-compose.yml` | Local full stack |
| `docker-stack.yml` | Docker Swarm deployment |
| `k8s/` | Kubernetes manifests (Deployments, Services, HPA) |
| `terraform/` | AWS EC2 provisioning |
| `ansible/` | VM setup and automated deploy |
| `monitoring/` | Prometheus, Grafana, alerts |
| `reports/` | SLI/SLO, incident, postmortem, end term report |

## Quick Start (Docker Compose)

```powershell
docker compose up --build -d
docker compose ps
```

| URL | Purpose |
|-----|---------|
| http://localhost | Frontend (all 6 services) |
| http://localhost:9091 | Prometheus |
| http://localhost:3000 | Grafana (`admin` / `admin`) |
| http://localhost:8001–8006 | Service health endpoints |

## Microservices

1. **Auth** (8001) — login simulation  
2. **Product** (8002) — catalog  
3. **Order** (8003) — orders + PostgreSQL  
4. **User Profile** (8004) — users  
5. **Notification** (8005) — alerts/email simulation  
6. **Payment** (8006) — payment simulation  

Supporting: **PostgreSQL**, **Redis**, **Prometheus**, **Grafana**

## Docker Swarm

```bash
docker swarm init
docker compose build
docker stack deploy -c docker-stack.yml sre
```

## Kubernetes

Build images, tag for K8s, apply manifests — see [DEPLOYMENT.md](DEPLOYMENT.md).

## Terraform (AWS VM)

```bash
cd terraform
terraform init && terraform plan && terraform apply
```

## Ansible (deploy to VM)

1. Set VM IP in `ansible/inventory/hosts.ini`
2. `ansible-playbook ansible/playbooks/site.yml`

## Incident Simulation

```powershell
$env:BROKEN_DB_CONFIG="true"
docker compose up -d --build order-service
# http://localhost:8003/health → 500

$env:BROKEN_DB_CONFIG="false"
docker compose up -d --build order-service
```

Details: `reports/assignment4_incident_report.md`, `reports/postmortem.md`

## End Term Submission

1. Run the stack and capture screenshots (containers, Prometheus, Grafana, incident, Terraform).
2. Export **`reports/end_term_project_report.md`** to PDF.
3. Upload **PDF with Git link** only (per assignment requirements).

## Reports

- `reports/end_term_project_report.md` — main end term document  
- `reports/sli_slo.md` — SLI/SLO definitions  
- `reports/assignment4_incident_report.md`  
- `reports/assignment5_terraform_report.md`  
- `reports/assignment6_automation_capacity_report.md`  
- `reports/postmortem.md`
