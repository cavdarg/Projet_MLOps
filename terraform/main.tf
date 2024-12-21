# Groupe de sécurité pour Grafana
resource "aws_security_group" "allow_grafana" {
  name        = "allow_grafana"
  description = "Allow Grafana traffic on port 3000"

  ingress {
    description = "Grafana access from anywhere"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Remplacez par votre IP pour restreindre l'accès (par exemple : ["203.0.113.0/32"])
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_grafana"
  }
}


# Groupe de sécurité pour le port 9090 (Prometheus)
resource "aws_security_group" "allow_prometheus" {
  name        = "allow_prometheus"
  description = "Allow Prometheus traffic on port 9090"

  ingress {
    description = "Prometheus access from anywhere"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Ou restreindre à votre IP pour plus de sécurité
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_prometheus"
  }
}

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
    aws_security_group.allow_http_s.id,
    aws_security_group.allow_prometheus.id,
    aws_security_group.allow_grafana.id
  ]

    # Configuration du volume root
  root_block_device {
    volume_size = 16       # Taille du volume root en Go
    volume_type = "gp2"    # Type du volume (gp2, gp3, io1, etc.)
    delete_on_termination = true  # Supprimer le volume à la terminaison de l'instance
  }


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
