# Groupe de sécurité pour le port 5000
resource "aws_security_group" "allow_api" {
  name        = "allow_api"
  description = "Allow API traffic on port 5000"

  ingress {
    description = "API access from anywhere"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_api"
  }
}

# Groupe de sécurité pour SSH
resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_ssh"
  }
}

# Groupe de sécurité pour HTTP et HTTPS
resource "aws_security_group" "allow_http_s" {
  name        = "allow_http_s"
  description = "Allow HTTP/S inbound traffic"

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_http_s"
  }
}



resource "aws_instance" "ml_api_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name


  # Références aux groupes de sécurité
  vpc_security_group_ids = [
    aws_security_group.allow_api.id,
    aws_security_group.allow_ssh.id,
    aws_security_group.allow_http_s.id
  ]


  tags = {
    Name = var.instance_name
  }

  # User data pour installer Docker
  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker
              EOF
}

output "instance_ip" {
  description = "Adresse IP publique de l'instance"
  value       = aws_instance.ml_api_instance.public_ip
}
