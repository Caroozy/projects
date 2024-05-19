terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.49.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-backend-daniel"
    key            = "app_backend.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }

}

provider "aws" {
  region = "eu-central-1"
}

variable "sg_ingress" {
  type = list(object({
    description = string
    port        = number
    cidr_block  = string
    protocol    = string
  }))

  default = [
    {
      description = "ingress allow SSH"
      port        = 22
      cidr_block  = "0.0.0.0/0" # Replace with self IP for better security.
      protocol    = "tcp"
    },
    {
      description = "ingress allow http"
      port        = 80
      cidr_block  = "0.0.0.0/0"
      protocol    = "tcp"
    }
  ]
}

variable "sg_egress" {
  type = list(object({
    description = string
    port        = number
    cidr_block  = string
    protocol    = string
  }))

  default = [
    {
      description = "egress allow outbound"
      port        = 0
      cidr_block  = "0.0.0.0/0"
      protocol    = "-1"
    }
  ]
}

resource "aws_security_group" "terraform_sg" {
  name = "terraform_learning_sg"

  dynamic "ingress" {
    for_each = var.sg_ingress
    iterator = sg

    content {
      from_port   = sg.value.port
      to_port     = sg.value.port
      protocol    = sg.value.protocol
      cidr_blocks = [sg.value.cidr_block]
    }
  }

  dynamic "egress" {
    for_each = var.sg_egress
    iterator = sg
    content {
      from_port   = sg.value.port
      to_port     = sg.value.port
      protocol    = sg.value.protocol
      cidr_blocks = [sg.value.cidr_block]
    }
  }
}

resource "aws_instance" "ubuntu_server" {
  instance_type          = "t2.micro"
  ami                    = "ami-01e444924a2233b07"
  vpc_security_group_ids = [aws_security_group.terraform_sg.id]

  user_data = <<-EOF
	#!/bin/bash
	# Add Docker's official GPG key:
	sudo apt-get update
	sudo apt-get install -y ca-certificates curl
	sudo install -m 0755 -d /etc/apt/keyrings
	sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
	sudo chmod a+r /etc/apt/keyrings/docker.asc

	echo \
	  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
	  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
	  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt-get update
	sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
	sudo usermod -aG docker ubuntu
	newgrp docker
	docker run -d -p 80:8989 --name weather_app --restart always caroozy/jenkins-weather:132
	EOF

  tags = {
    Name = "terraform_instance"
  }
}
