#!/usr/bin/env bash
set -e

# change directory to the one where this script resides.
cd "$(dirname "${BASH_SOURCE[0]}")"

EXPECTED_FILE="$(cat packer/index.html)"


# Verify 200 on index file

if [ "$(curl -s -o /dev/null -w "%{http_code} %header{Location}" http://http-demo.duane.cc)" = "301 https://http-demo.duane.cc/" ]; then
    echo "redirect verified"
else
    echo "redirect failed"
    exit 1
fi

if [ "$(curl -s https://http-demo.duane.cc/)" = "$EXPECTED_FILE" ]; then
    echo "index verified"
else
    echo "index failed"
    exit 1
fi

