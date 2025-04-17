output "public_ips" {
  value = aws_autoscaling_group.asg.instances[*].instance_id
}
