output "vpc_no" { value = ncloud_vpc.main.id }
output "server_subnet_no" { value = ncloud_subnet.server.id }
output "lb_subnet_no" { value = ncloud_subnet.lb.id }
