from fabric.api import task
from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import roles

from ade25.fabfiles import server
from ade25.fabfiles import project

from ade25.fabfiles.server import setup

env.use_ssh_config = True
env.forward_agent = True
env.port = '22222'
env.user = 'root'
env.hosts = ['z9']
env.webserver = '/opt/webserver/buildout.webserver'
env.code_root = '/opt/sites/hph/buildout.hph'
env.local_root = '/Users/eva/dev/hfph/buildout.hfph'
env.sitename = 'hph'
env.code_user = 'root'
env.prod_user = 'www'


env.roledefs = {
    'production': ['hph'],
    'staging': ['z9']
}


@task
@roles('production')
def deploy():
    """ Deploy current master to production server """
    project.site.update()
    project.site.restart()


@task
@roles('staging')
def stage():
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
    project.db.download_data()


@task
@roles('production')
def server_status():
    server.status.status()


@task
@roles('production')
def bootstrap():
    """ Bootstrap server and setup the webserver automagically """
    setup.install_system_libs()
    #setup.set_hostname()
    setup.configure_fs()
    setup.set_project_user_and_group('www', 'www')
    setup.configure_egg_cache()
    with cd('/opt'):
        setup.install_python()
        setup.generate_virtualenv(sitename='webserver')
    with cd('/opt/webserver'):
        setup.install_webserver()
    setup.setup_webserver_autostart()
