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

data "ncloud_subnet" "main" {
  id = var.main_subnet_no
}

data "ncloud_subnet" "lb" {
  id = var.lb_subnet_no
}

data "ncloud_nks_versions" "version" {
  filter {
    name   = "value"
    values = ["1.25.8"]
    regex  = true
  }
}

resource "ncloud_login_key" "loginkey" {
  key_name = "${var.ENV}-key"
}

resource "ncloud_nks_cluster" "cluster" {
  cluster_type         = "SVR.VNKS.STAND.C002.M008.NET.SSD.B050.G002"
  k8s_version          = data.ncloud_nks_versions.version.versions.0.value
  login_key_name       = ncloud_login_key.loginkey.key_name
  name                 = "${var.ENV}-cluster"
  lb_private_subnet_no = data.ncloud_subnet.lb.id
  kube_network_plugin  = "cilium"
  subnet_no_list       = [data.ncloud_subnet.main.id]
  vpc_no               = data.ncloud_vpc.main.id
  zone                 = "KR-2"
  public_network       = true
  log {
    audit = true
  }
}
