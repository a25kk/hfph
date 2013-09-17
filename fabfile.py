from fabric.api import task
from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import execute

from ade25.fabfiles import server
from ade25.fabfiles import project

from ade25.fabfiles import hotfix

env.use_ssh_config = True
env.forward_agent = True
env.port = '22222'
env.user = 'root'
env.hosts = ['zope9']
env.hostname = 'zope9'
env.webserver = '/opt/webserver/buildout.webserver'
env.code_root = '/opt/sites/hph/buildout.hph'
env.local_root = '/Users/sd/dev/hfph/buildout.hfph'
env.sitename = 'hph'
env.code_user = 'root'
env.prod_user = 'www'


@task
def deploy():
    """ Deploy current master to production server """
    project.site.update()
    project.site.restart()


@task
def deploy_staging():
    """ Deploy current master to staging server """
    project.site.update()
    with cd(env.code_root):
        run('bin/buildout -Nc staging.cfg')
    project.site.restart()


@task
def deploy_full():
    """ Deploy current master to production and run buildout """
    project.site.update()
    project.site.build()
    project.site.restart()


@task
def rebuild():
    """ Deploy current master and run full buildout """
    project.site.update()
    project.site.build_full()
    project.site.restart()


@task
def get_data():
    """ Copy live database for local development """
    project.db.download()
