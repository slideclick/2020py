#!/usr/bin/env sh
echo '$1 = ' $1 ###set arg1=%1
git checkout -- .
git checkout Dev
git fetch
git pull
git checkout -b $1  Dev