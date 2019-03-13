# -*- coding: utf-8 -*-
"""Module providing docker compose commands"""
from fabric import api
from fabric.api import task


@task
def build():
    """ Build docker container """
    build_dir = '{0}/build'.format(api.env.local_root)
    configuration = '-f {0}/docker-compose.yml'.format(build_dir)
    traefik = '-f {0}/docker-compose.traefik.yml'.format(build_dir)
    with api.lcd(api.env.local_root):
        api.local('docker-compose {0} {1} build'.format(
            configuration, traefik)
        )


@task
def run():
    """ Run docker container """
    build_dir = '{0}/build'.format(api.env.local_root)
    configuration = '-f {0}/docker-compose.yml'.format(build_dir)
    traefik = '-f {0}/docker-compose.traefik.yml'.format(build_dir)
    with api.lcd(api.env.local_root):
        api.local('docker-compose {0} {1} up'.format(
            configuration, traefik)
        )
