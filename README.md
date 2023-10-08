# Hochschule für Philosophie München


* `Source code @ GitHub <https://github.com/a25kk/hfph>`_
* `Production @ LRZ <https://www.hfph.de>`_
* `Staging @ KK <https://hfph.ade25.de>`_


## Installation

This buildout is intended to be used via the development profile to provide
a ready to work on setup. To get started with a new development environment
clone the buildout to your local machine and initialize the buildout:

``` bash
$ git clone git@github.com:username/hfph.git
$ cd ./hfph
$ b5 install
```

We use the globally installed task runner `b5` for the project. The buildout is intended to be used with a docker setup that mirrors the production environment. Therefore the build requires a local docker and traefik installation.

Alternatively you can use the provided installation script

```bash
chmod 777 ./bootstrap.sh
./bootstrap.sh
```
