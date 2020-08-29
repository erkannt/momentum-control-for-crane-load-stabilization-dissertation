#!/bin/bash
set -euo pipefail

function git_is_clean {
    git diff --exit-code > /dev/null \
    && git diff --cached --exit-code > /dev/null \
    &&  git ls-files --other --exclude-standard --directory > /dev/null
}

sha=$(git rev-parse --short HEAD)

if git_is_clean ; then
    echo "Version:" ${sha}
else
    echo "Version:" ${sha}" (unclean -- WIP)"
fi
