#!/usr/bin/env bash

set -e

# Clone the repository
echo "Checking for existing record_creation_flask_app folder, recreating the record_creation_flask_app repo"
if [ -d ~/record_creation_flask_app/ ]; then
  rm -rf record_creation_flask_app
fi

# Cloning the repository
git clone git@gitlab.com:ltts_members/record_creation_flask_app.git

#Changing  into Home Directory
cd ~/record_creation_flask_app

# Checking out the branch based on CI_COMMIT_REF_NAME
GIT_BRANCH=$(git symbolic-ref --short HEAD)
BRANCH=${1:-$GIT_BRANCH}
echo "⚙ Checking out Record Creation Flask App branch to ${BRANCH}"
git checkout --track origin/"${BRANCH}" || true

# Run the Script to run the docker
chmod +x run.sh
./run.sh