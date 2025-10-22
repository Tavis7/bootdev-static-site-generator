#!/bin/bash

# this is just a wrapper for the main.sh that boot.dev expects
./main.sh --no-server "$@"
./main.sh --no-server -- "/bootdev-static-site-generator" "docs"
