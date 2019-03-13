from fabric.api import task, run, cd, env


@task
def host_type():
    """ Server host type information """
    run('uname -s')


@task
def uptime():
    """ Server uptime """
    run('uptime')


@task
def load():
    """ Server average system load """
    run('cat /proc/loadavg')


@task
def memory():
    """ Server memory usage """
    run('free')


@task
def disk():
    """ Server disk and filesystem usage """
    run('df -ha')


@task
def supervisor():
    """ Server supervisord process status """
    with cd(env.webserver):
        run('bin/supervisorctl status')


@task
def status():
    """ Server status information """
    # General health of the server.
    uptime()
    load()
    memory()
    disk()
    supervisor()
