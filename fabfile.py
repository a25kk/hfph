import getpass
from fabric.api import task
from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import roles
from fabric.api import settings

from ade25.fabfiles import server
from ade25.fabfiles import project

from ade25.fabfiles.server import controls

from slacker import Slacker
slack = Slacker('xoxp-2440800772-2440800774-2520374751-468e84')

env.use_ssh_config = True
env.forward_agent = True
env.port = '22'
env.user = 'root'
env.hosts = ['z9']
env.webserver = '/opt/sites/hph/buildout.hph'
env.code_root = '/opt/sites/hph/buildout.hph'
env.local_root = '/Users/cb/dev/hph/buildout.hph'
env.sitename = 'hph'
env.code_user = 'root'
env.prod_user = 'www'
env.actor = 'Christoph Boehner'


env.roledefs = {
    'production': ['hph'],
    'staging': ['z9']
}


@task
@roles('production')
def restart():
    """ Restart all """
    project.cluster.restart_clients()


@task
@roles('production')
def restart_all():
    """ Restart all """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart all')


@task
@roles('production')
def restart_nginx():
    """ Restart Nginx """
    controls.restart_nginx()


@task
@roles('production')
def restart_varnish():
    """ Restart Varnish """
    controls.restart_varnish()


@task
@roles('production')
def restart_haproxy():
    """ Restart HAProxy """
    controls.restart_haproxy()


@task
@roles('production')
def ctl(*cmd):
    """Runs an arbitrary supervisorctl command."""
    with cd(env.code_root):
        run('nice bin/supervisorctl ' + ' '.join(cmd))


@task
@roles('production')
def deploy(actor=None):
    """ Deploy current master to production server """
    opts = dict(
        username=actor or env.get('actor') or getpass.getuser(),
    )
    controls.update()
    controls.build()
    project.cluster.restart_clients()
    msg = ('[hph] %(username)s deployed tp production' % opts)
    user = 'fabric'
    icon = ':shipit:'
    slack.chat.post_message('#general', msg, username=user, icon_emoji=icon)


@task
@roles('staging')
def stage(actor=None):
    """ Deploy current master to staging server """
    opts = dict(
        username=actor or env.get('actor') or getpass.getuser(),
    )
    with settings(port=22222, webserver='/opt/webserver/buildout.webserver'):
        project.site.update()
        with cd(env.code_root):
            run('bin/buildout -Nc staging.cfg')
        project.site.restart()
    msg = ('[z9] Christoph Boehner deployed hph' % opts)
    user = 'fabric'
    icon = ':shipit:'
    slack.chat.post_message('#general', msg, username=user, icon_emoji=icon)


@task
@roles('staging')
def deploy_full():
    """ Deploy current master to production and run buildout """
    with settings(port=22222, webserver='/opt/webserver/buildout.webserver'):
        project.site.update()
        project.site.build()
        project.site.restart()


@task
def rebuild():
    """ Deploy current master and run full buildout """
    with settings(port=22):
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
