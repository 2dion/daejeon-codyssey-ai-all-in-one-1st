#!/bin/zsh
PS4='$ '
set -x
mkdir -p practice/cli-capture-20261102
cd practice/cli-capture-20261102
pwd
echo 'hello codyssey' > original.txt
touch empty.txt
ls -la
cat original.txt
cp original.txt copy.txt
ls -l
cat copy.txt
