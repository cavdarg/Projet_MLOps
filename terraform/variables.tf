variable "instance_name" {
  default = "ml-api-instance"
}

variable "instance_type" {
  default = "t2.micro"  
}

variable "ami_id" {
  default = "ami-0e2c8caa4b6378d8c"  # Ubuntu 24.04 LTS
}

variable "key_name" {
  default = "myKey"  # Nom de la clé SSH 
}

variable "public_key_path" {
  default = "./myKey.pem"  # Chemin vers votre clé privée
}
