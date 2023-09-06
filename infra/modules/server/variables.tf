variable "NCP_ACCESS_KEY" {}
variable "NCP_SECRET_KEY" {}
variable "ENV" {}
variable "NAME" {}
variable "vpc_no" {}
variable "subnet_no" {}
variable "private_ip" {}
variable "port" {}
variable "init_env" {}

variable "server_image_product_code" {
  type    = string
  default = "SW.VSVR.OS.LNX64.UBNTU.SVR2004.B050"
}

