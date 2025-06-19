#!/bin/bash

get_config () {
    echo "${RUNNER_CONFIG}" | jq -r ".$1"
}

apt_init () {
    # If using apt, make sure to use https
    sed -i 's|http://|https://|g' /etc/apt/sources.list

    apt-get update
    apt-get upgrade -y
    apt-get install -y git python3 python3-pip python3-venv jq

    apt_after_install
}

# Executing when required packages like jq are installed
apt_after_install () {
    additionalPackages=$(get_config additionalPackages)
    if [ -n "$additionalPackages" ]; then
        apt-get install -y $additionalPackages
    fi
}

apt-get --version && apt_init

mkdir -p /runner

addgroup appgroup && adduser --disabled-password --gecos "" --ingroup appgroup appuser
chown appuser:appgroup /runner

challengeRepo=$(get_config challengeRepo)
git clone "$challengeRepo" /runner

python3 -m venv /runner/venv
source /runner/venv/bin/activate
pip install -r requirements.txt