#!/bin/sh
virtualenv --clear .
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" ./bin/pip install cryptography
./bin/pip install zc.buildout
./bin/buildout $*