from fabric.api import cd
from fabric.api import task
from fabric.api import env
from fabric.api import run


@task
def restart_cluster():
    with cd(env.webserver):
        for site in env.hosted_sites:
            run('nice bin/supervisorctl restart instance-%s' % site)


@task
def restart_zeoserver():
    with cd(env.webserver):
        run('nice bin/supervisorctl restart zeoserver')


@task
def restart_clients():
    with cd(env.webserver):
        run('nice bin/supervisorctl restart instance1')
        run('nice bin/supervisorctl restart instance2')
        run('nice bin/supervisorctl restart instance3')
        run('nice bin/supervisorctl restart instance4')
