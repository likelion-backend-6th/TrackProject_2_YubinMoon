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

data "ncloud_server_image" "image" {
  filter {
    name   = "product_name"
    values = ["ubuntu-20.04"]
  }
}

data "ncloud_server_product" "product" {
  server_image_product_code = data.ncloud_server_image.image.product_code

  filter {
    name   = "product_type"
    values = ["STAND"]
  }

  filter {
    name   = "cpu_count"
    values = [2]
  }

  filter {
    name   = "memory_size"
    values = ["8GB"]
  }

  filter {
    name   = "product_code"
    values = ["SSD"]
    regex  = true
  }
}

resource "ncloud_nks_node_pool" "node_pool" {
  cluster_uuid   = var.cluster_uuid
  node_pool_name = "${var.ENV}-node"
  node_count     = 1
  product_code   = data.ncloud_server_product.product.product_code

  autoscale {
    enabled = true
    min     = 1
    max     = 2
  }

  lifecycle {
    ignore_changes = [node_count, subnet_no_list]
  }
}
