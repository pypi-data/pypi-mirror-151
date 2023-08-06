#!/bin/bash
set -e -u -o pipefail

git config core.hooksPath $PWD/.githooks

exit 0
