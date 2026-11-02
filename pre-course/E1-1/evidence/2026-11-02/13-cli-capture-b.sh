#!/bin/zsh
PS4='$ '
set -x
cd practice/cli-capture-20261102
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
