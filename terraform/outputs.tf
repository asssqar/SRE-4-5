output "instance_public_ip" {
  description = "Public IP of provisioned VM"
  value       = aws_instance.sre_vm.public_ip
}

output "instance_id" {
  description = "ID of provisioned VM"
  value       = aws_instance.sre_vm.id
}
