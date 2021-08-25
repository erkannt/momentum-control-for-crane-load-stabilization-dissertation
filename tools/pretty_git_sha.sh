#!/bin/bash
set -euo pipefail

function git_is_clean {
    git diff --exit-code > /dev/null \
    && git diff --cached --exit-code > /dev/null \
    &&  git ls-files --other --exclude-standard --directory > /dev/null
}

sha=$(git rev-parse --short HEAD)
date=$(git log -1 --date=short --format=%cd)

if git_is_clean ; then
    echo "Version:" ${date} "("${sha}")"
else
    echo "Version:" ${date} "(unclean -- WIP)"
fi
