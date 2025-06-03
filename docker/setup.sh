#!/bin/bash

apt update && apt upgrade

sudo apt-get install apt-transport-https ca-certificates curl gnupg2
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/debian stretch stable" | sudo tee -a /etc/apt/sources.list
sudo apt update
sudo apt install docker-ce

sudo systemctl status docker
# docker --version

sudo usermod -aG docker ${USER}
sudo su - ${USER}

LATEST_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d '"' -f 4)

if [ -z "$LATEST_VERSION" ]; then
    LATEST_VERSION=v2.36.0
fi

sudo curl -L https://github.com/docker/compose/releases/download/${LATEST_VERSION}/docker-compose-Linux-x86_64 -o /usr/local/bin/docker-compose

sudo chmod x /usr/local/bin/docker-compose

docker --version
docker-compose --version