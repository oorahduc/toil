#!/usr/bin/env bash

mkdir ~/.toil/
cp ./db/toil.db ~/.toil/
echo "SQLite db created at ~/.toil/toil.db"
echo "Next step: python3 setup.py install"
