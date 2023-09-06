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

locals {
  ENV = "${var.ENV}-${var.NAME}"
}

data "ncloud_vpc" "main" {
  id = var.vpc_no
}

data "ncloud_subnet" "main" {
  id = var.subnet_no
}

data "ncloud_server_product" "product" {
  server_image_product_code = var.server_image_product_code

  filter {
    name   = "product_code"
    values = ["SSD"]
    regex  = true
  }
  filter {
    name   = "cpu_count"
    values = ["2"]
  }
  filter {
    name   = "product_type"
    values = ["HICPU"]
  }
}

resource "ncloud_server" "server" {
  subnet_no                 = data.ncloud_subnet.main.id
  name                      = "${local.ENV}-server"
  server_image_product_code = var.server_image_product_code
  server_product_code       = data.ncloud_server_product.product.id
  login_key_name            = ncloud_login_key.loginkey.key_name
  init_script_no            = ncloud_init_script.init.init_script_no

  network_interface {
    network_interface_no = ncloud_network_interface.main.network_interface_no
    order                = 0
  }
}

resource "ncloud_login_key" "loginkey" {
  key_name = "${local.ENV}-key"
}

resource "ncloud_init_script" "init" {
  name    = "${local.ENV}-init"
  content = templatefile("${path.module}/${var.NAME}_init_script.sh", var.init_env)
}

resource "ncloud_network_interface" "main" {
  name                  = local.ENV
  subnet_no             = data.ncloud_subnet.main.subnet_no
  private_ip            = var.private_ip
  access_control_groups = [data.ncloud_vpc.main.default_access_control_group_no, ncloud_access_control_group.acg.access_control_group_no]
}

resource "ncloud_access_control_group" "acg" {
  name   = local.ENV
  vpc_no = data.ncloud_vpc.main.vpc_no
}

resource "ncloud_access_control_group_rule" "main" {
  access_control_group_no = ncloud_access_control_group.acg.id

  inbound {
    protocol   = "TCP"
    ip_block   = "0.0.0.0/0"
    port_range = var.port
  }
}

resource "ncloud_public_ip" "public_ip" {
  server_instance_no = ncloud_server.server.id
}
