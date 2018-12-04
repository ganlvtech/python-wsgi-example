#!/usr/bin/env bash

pushd $(dirname $0)
cd src/

export GOOS=linux
go build -o ../bin/main
chmod +x ../bin/main

export GOOS=windows
go build -o ../bin/main.exe
chmod +x ../bin/main.exe

export GOOS=

popd
