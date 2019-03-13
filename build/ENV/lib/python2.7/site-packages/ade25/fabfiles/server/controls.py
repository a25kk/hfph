from fabric.api import cd
from fabric.api import task
from fabric.api import env
from fabric.api import run


@task
def restart_all():
    """ Restart all """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart all')


@task
def restart_nginx():
    """ Restart Nginx """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart nginx')


@task
def restart_varnish():
    """ Restart Varnish """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart varnish')


@task
def restart_haproxy():
    """ Restart HAProxy """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart haproxy')


@task
def reload_supervisor():
    """ Reload supervisor configuration """
    with cd(env.webserver):
        run('bin/supervisorctl reread')
        run('bin/supervisorctl update')


@task
def update():
    """ Update buildout from git/master """
    with cd(env.code_root):
        run('nice git pull')


@task
def build():
    """ Buildout deployment profile (no update) """
    with cd(env.code_root):
        run('bin/buildout -Nc deployment.cfg')


@task
def build_full():
    """ Buildout deployment profile (full) """
    with cd(env.code_root):
        run('bin/buildout -c deployment.cfg')
