#!/bin/zsh
PS4='$ '
set -x
umask
mkdir -p practice/permission-dir
touch practice/permission-file
ls -l practice/permission-file
ls -ld practice/permission-dir
chmod 600 practice/permission-file
ls -l practice/permission-file
chmod 644 practice/permission-file
ls -l practice/permission-file
chmod 700 practice/permission-dir
ls -ld practice/permission-dir
chmod 755 practice/permission-dir
ls -ld practice/permission-dir
