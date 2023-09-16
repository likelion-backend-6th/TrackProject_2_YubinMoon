terraform {

  backend "s3" {
    shared_credentials_file     = ".credentials"
    bucket                      = "tractproject1"
    key                         = "k8s/terraform.tfstate"
    region                      = "kr-standard"
    endpoint                    = "https://kr.object.ncloudstorage.com"
    skip_region_validation      = true
    skip_credentials_validation = true
  }

  required_providers {
    ncloud = {
      source = "NaverCloudPlatform/ncloud"
    }
  }
  required_version = ">= 0.13"
}

locals {
  ENV = "tweet-k8s"
}

// Configure the ncloud provider
provider "ncloud" {
  access_key  = var.NCP_ACCESS_KEY
  secret_key  = var.NCP_SECRET_KEY
  region      = "KR"
  support_vpc = true
}

module "network" {
  source         = "../modules/network"
  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  ENV            = local.ENV
}

module "cluster" {
  source         = "../modules/cluster"
  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  ENV            = local.ENV
  vpc_no         = module.network.vpc_no
  main_subnet_no = module.network.main_subnet_no
  lb_subnet_no   = module.network.lb_subnet_no
}

module "node" {
  source         = "../modules/node"
  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  ENV            = local.ENV
  cluster_uuid   = module.cluster.cluster_uuid
}
