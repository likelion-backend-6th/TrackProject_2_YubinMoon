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

resource "ncloud_lb" "main" {
  name           = "${var.ENV}-lb"
  network_type   = "PUBLIC"
  type           = "NETWORK_PROXY"
  subnet_no_list = [var.subnet_no]
}
