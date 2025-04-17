data "aws_instances" "asg_instances" {
  depends_on = [aws_autoscaling_group.asg]

  filter {
    name   = "tag:Name"
    values = ["file-converter-instance"]
  }

  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
}

output "public_ips" {
  value = data.aws_instances.asg_instances.public_ips
}

