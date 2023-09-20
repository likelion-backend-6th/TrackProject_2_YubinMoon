output "vpc_no" { value = ncloud_vpc.main.id }
output "main_subnet_no" { value = ncloud_subnet.main.id }
output "lb_subnet_no" { value = ncloud_subnet.lb.id }
