# Assignment 4-5: SRE + IaC Project

This repository contains a containerized microservices system with Terraform infrastructure provisioning, monitoring stack, and incident response simulation artifacts.

## Project Structure

- `services/`: FastAPI microservices (`auth`, `product`, `order`, `user`, `chat`)
- `frontend/`: Nginx-served web frontend
- `monitoring/`: Prometheus configuration
- `terraform/`: IaC files (`main.tf`, `variables.tf`, `outputs.tf`, `terraform.tfvars`)
- `reports/`: Assignment 4 and 5 reports
- `docker-compose.yml`: Full stack deployment

## Local Deployment (Docker Compose)

1. Build and run:
   - `docker compose up --build -d`
2. Verify:
   - Frontend: `http://localhost`
   - Prometheus: `http://localhost:9091`
   - Grafana: `http://localhost:3000`
3. Check services:
   - Auth: `http://localhost:8001/health`
   - Product: `http://localhost:8002/health`
   - Order: `http://localhost:8003/health`
   - User: `http://localhost:8004/health`
   - Chat: `http://localhost:8005/health`

## Unified Frontend (One Page for 5 Services)

Open `http://localhost` to use a single control panel that works with all services:
- Auth: health + GET/POST login
- Product: list + create product
- Order: health/list + create order
- User: list + create user
- Chat: list + send message

The frontend uses Nginx reverse proxy routes (`/api/auth/*`, `/api/product/*`, `/api/order/*`, `/api/user/*`, `/api/chat/*`) so all requests work from one page without CORS issues.

## Incident Simulation (Assignment 4)

Simulate an Order Service DB misconfiguration:

1. Stop stack: `docker compose down`
2. Set broken config:
   - PowerShell: `$env:BROKEN_DB_CONFIG="true"`
3. Start stack: `docker compose up --build -d`
4. Validate failure:
   - `http://localhost:8003/health` returns HTTP 500
5. Mitigate:
   - PowerShell: `$env:BROKEN_DB_CONFIG="false"`
   - Restart order service: `docker compose up -d --build order-service`
6. Confirm restoration:
   - `http://localhost:8003/health` returns HTTP 200

## Terraform Deployment (Assignment 5)

1. Update `terraform/terraform.tfvars` (`key_name`, AMI if needed).
2. Run:
   - `cd terraform`
   - `terraform init`
   - `terraform plan`
   - `terraform apply`
3. Capture public IP from output `instance_public_ip`.

## Required Evidence (Screenshots)

Collect screenshots for submission:
- Running containers (`docker compose ps`)
- Prometheus targets in UP state
- Grafana dashboard panels
- Order service failure during incident
- Order service restored after mitigation
- Terraform `plan` and `apply` outputs
