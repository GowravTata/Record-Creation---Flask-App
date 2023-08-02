#!/usr/bin/env bash

set -e

# Clone the repository
echo "Checking for existing Record-Creation---Flask-App folder , recreating the Record-Creation---Flask-App repo"
if [ -d ~/Record-Creation---Flask-App/ ]; then
  rm -rf Record-Creation---Flask-App
fi

# Cloning the repository
git clone https://github.com/GowravTata/Record-Creation---Flask-App.git

#Changing  into Home Directory
cd Record-Creation---Flask-App/

# Use the below block only when the name of the branch is passed
# Checking out the branch based on CI_COMMIT_REF_NAME
GIT_BRANCH=$(git symbolic-ref --short HEAD)
BRANCH=${1:-$GIT_BRANCH}
echo "⚙ Checking out Record Creation Flask App branch to ${BRANCH}"
git checkout --track origin/"${BRANCH}" || true

# Build the Docker file
sudo docker-compose up -d --build