#!/bin/bash
set -e -u -o pipefail

git config core.hooksPath $PWD/.git/hooks

exit 0
