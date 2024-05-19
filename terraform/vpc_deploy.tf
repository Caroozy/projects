terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.49.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-backend-daniel"
    key            = "vpc_backend.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }

}

provider "aws" {
  region = "eu-central-1"
}

variable "pub_subnet_cidrs" {
  type        = string
  description = "public subnet cidr blocks"
  default     = "10.0.1.0/24"
}

variable "prv_subnet_cidrs" {
  type        = string
  description = "private subnet cidr blocks"
  default     = "10.0.2.0/24"
}

resource "aws_vpc" "tf_vpc" {
  cidr_block = "10.0.0.0/16"
  tags       = { Name = "Terraform VPC" }
}

resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.tf_vpc.id
  cidr_block = var.pub_subnet_cidrs

  tags = {
    Name = "tf pub subnet"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.tf_vpc.id
  cidr_block = var.prv_subnet_cidrs

  tags = {
    Name = "tf private subnet"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.tf_vpc.id

  tags = { Name = "tf vpc igw" }
}

resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.tf_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "tf route table"
  }
}

resource "aws_route_table_association" "pub_sub_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.rt.id
}
