terraform {

  backend "s3" {
    shared_credentials_file     = ".credentials"
    bucket                      = "tractproject1"
    key                         = "prod/terraform.tfstate"
    region                      = "kr-standard"
    endpoint                    = "https://kr.object.ncloudstorage.com"
    skip_region_validation      = true
    skip_credentials_validation = true
  }

  required_providers {
    ncloud = {
      source = "NaverCloudPlatform/ncloud"
    }

    ssh = {
      source  = "loafoe/ssh"
      version = "2.6.0"
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

provider "ssh" {}

locals {
  ENV = "prod"
}

data "ncloud_subnet" "main" {
  id = module.network.server_subnet_no
}

module "network" {
  source = "../modules/network"

  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  ENV            = local.ENV
}

module "lb_create" {
  source = "../modules/lb_create"

  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  ENV            = local.ENV
  subnet_no      = module.network.lb_subnet_no
}

module "db_server" {
  source = "../modules/server"

  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  ENV            = local.ENV
  NAME           = "db"
  vpc_no         = module.network.vpc_no
  subnet_no      = module.network.server_subnet_no
  private_ip     = cidrhost(data.ncloud_subnet.main.subnet, 6)
  port           = var.postgres_port
  init_env = {
    password          = var.password
    postgres_db       = var.postgres_db
    postgres_user     = var.postgres_user
    postgres_password = var.postgres_password
    postgres_port     = var.postgres_port
    ncr_registry      = var.ncr_registry
    docker_user       = var.NCP_ACCESS_KEY
    docker_password   = var.NCP_SECRET_KEY
  }
}

module "be_server" {
  source = "../modules/server"

  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  ENV            = local.ENV
  NAME           = "be"
  vpc_no         = module.network.vpc_no
  subnet_no      = module.network.server_subnet_no
  private_ip     = cidrhost(data.ncloud_subnet.main.subnet, 7)
  port           = "8000"
  init_env = {
    password             = var.password
    postgres_db          = var.postgres_db
    postgres_user        = var.postgres_user
    postgres_password    = var.postgres_password
    postgres_port        = var.postgres_port
    ncr_registry         = var.ncr_registry
    docker_user          = var.NCP_ACCESS_KEY
    docker_password      = var.NCP_SECRET_KEY
    db_host              = module.db_server.public_ip
    django_secret_key    = var.django_secret_key
    django_mode          = local.ENV
    django_allowed_hosts = module.lb_create.domain
  }
}

module "lb_setting" {
  source = "../modules/lb_setting"

  NCP_ACCESS_KEY = var.NCP_ACCESS_KEY
  NCP_SECRET_KEY = var.NCP_SECRET_KEY
  vpc_no         = module.network.vpc_no
  lb_no          = module.lb_create.lb_no
  server_no_list = [module.be_server.server_no]
}

resource "ssh_resource" "init_db" {
  depends_on = [module.db_server]
  when       = "create"

  host     = module.db_server.public_ip
  user     = "terry"
  password = var.password

  timeout     = "30s"
  retry_delay = "5s"

  file {
    source      = "${path.module}/set_db_server.sh"
    destination = "/home/terry/set_db.sh"
    permissions = "0700"
  }

  commands = [
    ". set_db.sh"
  ]
}

resource "ssh_resource" "init_be" {
  depends_on = [module.be_server]
  when       = "create"

  host     = module.be_server.public_ip
  user     = "terry"
  password = var.password

  timeout     = "30s"
  retry_delay = "5s"

  file {
    source      = "${path.module}/set_be_server.sh"
    destination = "/home/terry/set_be.sh"
    permissions = "0700"
  }

  commands = [
    ". set_be.sh"
  ]
}
