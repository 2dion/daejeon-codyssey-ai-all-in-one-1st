#!/bin/zsh
PS4='$ '
set -x
pwd
ls -la
mkdir -p practice/cli-proof-20261102
cd practice/cli-proof-20261102
pwd
echo 'hello codyssey' > original.txt
touch empty.txt
ls -la
cat original.txt
cp original.txt copy.txt
ls -l
cat copy.txt
mv copy.txt renamed.txt
ls -l
mkdir moved
mv renamed.txt moved/
ls -la . moved
rm moved/renamed.txt
ls -la moved
rmdir moved
ls -la
cd ../..
pwd
