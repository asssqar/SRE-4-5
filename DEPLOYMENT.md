# Deployment Guide — End Term SRE Project

## Prerequisites

- Docker Desktop (Compose v2)
- Optional: Terraform >= 1.5, AWS account, Ansible, Kubernetes cluster (minikube/kind)

## 1. Docker Compose (primary demo)

```powershell
cd c:\Users\asqar\Desktop\SRE-4
docker compose up --build -d
docker compose ps
```

Validate health for all six services and open http://localhost.

## 2. Docker Swarm

```bash
docker swarm init
docker compose build
docker stack deploy -c docker-stack.yml sre
docker stack services sre
```

## 3. Kubernetes

Build images from project root:

```powershell
docker compose build
docker tag sre-4-auth-service sre-auth-service:latest
docker tag sre-4-product-service sre-product-service:latest
docker tag sre-4-order-service sre-order-service:latest
docker tag sre-4-user-service sre-user-service:latest
docker tag sre-4-notification-service sre-notification-service:latest
docker tag sre-4-payment-service sre-payment-service:latest
docker tag sre-4-frontend sre-frontend:latest
```

For minikube/kind, load images into the cluster, then:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/microservices.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/monitoring.yaml
kubectl apply -f k8s/hpa-order.yaml
```

Frontend NodePort: `30080`. Prometheus NodePort: `30091`.

## 4. Terraform (AWS)

1. Configure `terraform/terraform.tfvars` (`key_name`, region, AMI).
2. `terraform init && terraform plan && terraform apply`
3. Use `instance_public_ip` for SSH and Ansible inventory.

## 5. Ansible

1. Edit `ansible/inventory/hosts.ini` — set `ansible_host` to Terraform public IP.
2. Ensure SSH access as `ansible_user`.
3. Run from project root:

```bash
ansible-playbook ansible/playbooks/site.yml
```

## 6. Monitoring Validation

1. Prometheus → Status → Targets (all `UP`)
2. Grafana → dashboard **Microservices Overview (SRE)**
3. Prometheus → Alerts (rules loaded)

## 7. Incident Drill

```powershell
$env:BROKEN_DB_CONFIG="true"
docker compose up -d --build order-service
```

Observe HTTP 500 and alert `OrderServiceDBNotReady`. Recover with `BROKEN_DB_CONFIG=false` and restart order-service.

## 8. Load Test (capacity planning)

```powershell
1..200 | % { Invoke-WebRequest http://localhost/api/order/orders | Out-Null }
```

Capture Grafana screenshots during load.

## 9. Submission PDF

Export `reports/end_term_project_report.md` to PDF. Include Git link: https://github.com/asssqar/SRE-4-5.git and screenshots listed in the report checklist.
