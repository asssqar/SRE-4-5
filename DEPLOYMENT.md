# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Terraform >= 1.5 installed
- AWS account and key pair for EC2

## Step 1: Run Application Stack

1. From project root:
   - `docker compose up --build -d`
2. Check status:
   - `docker compose ps`
3. Open:
   - Frontend: `http://localhost`
   - Prometheus: `http://localhost:9090`
   - Grafana: `http://localhost:3000`

## Step 2: Validate Monitoring

1. Prometheus -> **Status > Targets**
2. Confirm all service targets are `UP`
3. In Grafana:
   - Add Prometheus datasource: `http://prometheus:9090`
   - Create panel with query: `rate(order_requests_total[1m])`

## Step 3: Execute Incident Simulation

1. Inject failure:
   - PowerShell: `$env:BROKEN_DB_CONFIG="true"`
   - `docker compose up -d --build order-service`
2. Observe:
   - `http://localhost:8003/health` -> 500
   - Prometheus errors increase for `order_errors_total`
3. Mitigate:
   - `$env:BROKEN_DB_CONFIG="false"`
   - `docker compose up -d --build order-service`
4. Restore:
   - `http://localhost:8003/health` -> 200

## Step 4: Provision Infrastructure via Terraform

1. `cd terraform`
2. `terraform init`
3. `terraform plan`
4. `terraform apply`
5. Save output with public IP and instance ID
