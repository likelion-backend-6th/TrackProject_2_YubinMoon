#!/bin/bash

USERNAME="terry"
USER_HOME="/home/$USERNAME"
PASSWORD=${password}

# useradd
useradd -m -s /bin/bash $USERNAME
# password
echo "$USERNAME:$PASSWORD" | chpasswd
# sudo with no password
echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >>/etc/sudoers
# update
apt-get update
# set docker
apt-get install -y docker.io
usermod -aG docker $USERNAME

ENV_PATH=$USER_HOME/.env

touch $ENV_PATH

echo "POSTGRES_DB=${postgres_db}" >>$ENV_PATH
echo "POSTGRES_USER=${postgres_user}" >>$ENV_PATH
echo "POSTGRES_PASSWORD=${postgres_password}" >>$ENV_PATH
echo "POSTGRES_PORT=${postgres_port}" >>$ENV_PATH
echo "NCR_REGISTRY=${ncr_registry}" >>$ENV_PATH
echo "DOCKER_USER=${docker_user}" >>$ENV_PATH
echo "DOCKER_PASSWORD=${docker_password}" >>$ENV_PATH
