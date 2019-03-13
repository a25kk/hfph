from fabric.api import *


@task
def update():
    """ Update buildout from git/master """
    with cd(env.code_root):
        run('nice git pull')


@task
def develop():
    """ Update source packages """
    with cd(env.code_root):
        run('nice bin/develop up')


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


@task
def restart_zope():
    """ Restart zope instance directly """
    with cd(env.code_root):
        run('bin/instance restart')


@task
def restart():
    """ Restart instance """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart instance-%(sitename)s' % env)
