# File built up from the following tutorial: https://developer.hashicorp.com/packer/tutorials/aws-get-started/aws-get-started-build-image

packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

# This is the base image for the build--owner is Canonical.
source "amazon-ebs" "ubuntu" {
  ami_name      = "http-demo-{{timestamp}}"
  instance_type = "t2.micro"
  region        = "us-west-2"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  ssh_username = "ubuntu"
}

# This is the image being built.
build {
  name = "http-demo-ubuntu-aws"
  sources = [
    "source.amazon-ebs.ubuntu"
  ]

  # Copy nginx configuration to home directory...
  provisioner "file" {
    source      = "nginx.conf"
    destination = "/home/ubuntu/nginx.conf"
  }

  # ...and the requested index file.
  provisioner "file" {
    source      = "index.html"
    destination = "/home/ubuntu/index.html"
  }


  # Install nginx, copy the files from the home directory to their final resting place, and restart nginx.
  provisioner "shell" {
    environment_vars = []
    inline = [
      "echo --- Installing nginx",
      "sudo apt update -yq",
      "sudo apt upgrade -yq",
      "sudo apt install -yq nginx",
      "echo --- Removing existing index file...",
      "sudo rm /var/www/html/index.nginx-debian.html",
      "echo --- Copying files...",
      "sudo cp /home/ubuntu/nginx.conf /etc/nginx/nginx.conf",
      "sudo cp /home/ubuntu/index.html /var/www/html/index.html",
      "echo --- Restarting nginx...",
      "sudo systemctl restart nginx",
      "echo --- done"
    ]
  }
}

