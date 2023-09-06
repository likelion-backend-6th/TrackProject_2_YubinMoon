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

resource "ncloud_vpc" "main" {
  name            = "${var.ENV}-vpc"
  ipv4_cidr_block = "10.0.0.0/16"
}

resource "ncloud_subnet" "server" {
  name           = "${var.ENV}-server-subnet"
  vpc_no         = ncloud_vpc.main.id
  subnet         = cidrsubnet(ncloud_vpc.main.ipv4_cidr_block, 8, 1)
  zone           = "KR-2"
  network_acl_no = ncloud_vpc.main.default_network_acl_no
  subnet_type    = "PUBLIC"
  usage_type     = "GEN"
}

resource "ncloud_subnet" "lb" {
  name           = "${var.ENV}-lb-subnet"
  vpc_no         = ncloud_vpc.main.id
  subnet         = cidrsubnet(ncloud_vpc.main.ipv4_cidr_block, 8, 2)
  zone           = "KR-2"
  network_acl_no = ncloud_vpc.main.default_network_acl_no
  subnet_type    = "PRIVATE"
  usage_type     = "LOADB"
}

