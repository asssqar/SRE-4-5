# Assignment 5 Terraform Report

## Objective

Provision a reproducible VM-based infrastructure using Terraform and expose required ports for application and observability.

## Implemented Files

- `terraform/main.tf`
- `terraform/variables.tf`
- `terraform/outputs.tf`
- `terraform/terraform.tfvars`

## Provisioned Resources

1. EC2 instance (`aws_instance.sre_vm`)
2. Security group (`aws_security_group.sre_sg`) with inbound rules:
   - SSH: 22
   - HTTP: 80
   - Grafana: 3000
   - Prometheus: 9091

## Reproducibility Workflow

1. `terraform init`
2. `terraform plan`
3. `terraform apply`

All infrastructure is defined declaratively and can be recreated in a clean environment using the same configuration.

## Output Values

- `instance_public_ip`
- `instance_id`

These outputs are used for deployment validation and remote access.
