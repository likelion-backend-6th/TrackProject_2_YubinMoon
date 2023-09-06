terraform {
  required_providers {
    ncloud = {
      source = "NaverCloudPlatform/ncloud"
    }
  }
  required_version = ">= 0.13"
}

// Configure the ncloud provider
provider "ncloud" {
  access_key  = var.NCP_ACCESS_KEY
  secret_key  = var.NCP_SECRET_KEY
  region      = "KR"
  support_vpc = true
}

data "ncloud_vpc" "main" {
  id = var.vpc_no
}

data "ncloud_lb" "main" {
  id = var.lb_no
}

resource "ncloud_lb_listener" "main" {
  load_balancer_no = data.ncloud_lb.main.load_balancer_no
  protocol         = "TCP"
  port             = 80
  target_group_no  = ncloud_lb_target_group.main.target_group_no
}

resource "ncloud_lb_target_group" "main" {
  vpc_no      = data.ncloud_vpc.main.vpc_no
  protocol    = "PROXY_TCP"
  target_type = "VSVR"
  port        = 8000
  health_check {
    protocol       = "TCP"
    http_method    = "GET"
    port           = 8000
    url_path       = "/health/"
    cycle          = 30
    up_threshold   = 2
    down_threshold = 2
  }
  algorithm_type = "RR"
  lifecycle {
    ignore_changes = [health_check]
  }
}

resource "ncloud_lb_target_group_attachment" "test" {
  target_group_no = ncloud_lb_target_group.main.target_group_no
  target_no_list  = var.server_no_list
}
