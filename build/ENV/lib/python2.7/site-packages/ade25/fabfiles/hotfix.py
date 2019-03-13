from collections import OrderedDict
from ConfigParser import ConfigParser

from cuisine import *
from fabric.api import env
from fabric.api import task
from fabric.api import cd
from fabric.api import run

from fabric.contrib.files import append
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project


@task
def close_firewall():
    """ Setup firewall and block everything but SSH and HTTP(S) """
    run('apt-get install ufw')
    run('ufw limit 22/tcp')
    run('ufw limit 22222/tcp')
    run('ufw allow 80/tcp')
    run('ufw allow 443/tcp')
    run('ufw enable')


@task
def process_hotfix(path=None):
    """ Process hotfix for all hosted sites """
    idx = 0
    for site in env.hosted_sites:
        apply_hotfix(
            sitename=site,
            path=path
        )
        print 'Processed hotfix for %s' % site
        idx += 1
    print 'Hotfixed %s sites on %s' % (idx, env.hostname)


@task
def apply_hotfix(sitename=None, path=None):
    """ Hotfix a single site/buildout """
    if sitename is None:
        print('A sitename is required')
    else:
        remote_path = ('/opt/sites/%s/buildout.%s' % (sitename, sitename))
        rsync_project(
            remote_dir='{0}/products/'.format(remote_path),
            local_dir=path
        )


@task
def prepare_sites():
    """ Add hotfix products directory """
    for site in env.hosted_sites:
        print('Prepare {0} for hotfixes'.format(site))
        location = '/opt/sites/{0}/buildout.{0}'.format(site)
        with cd(location):
            if exists('./products'):
                print '%s site already prepared' % site
            else:
                run('mkdir products')
                with cd('products'):
                    run('touch .gitkeep')
                    append('.gitkeep', '# make non empty dir')
                with cd('./parts/instance/etc'):
                    product_dir = 'products {0}/products'.format(location)
                    run('echo -e "\n{0}" >> zope.conf'.format(product_dir))
                with cd(env.webserver):
                    run('bin/supervisorctl restart instance-{0}'.format(site))
        print('Please fix the project buildouts to include products dir')


@task
def update_package_list(filename='packages.cfg', addon=None, site='Plone'):
    """ Append package to buildout eggs

        @param filename: the configuration file to update
        @param addon: the package name to append
        @param site: name of the site to be updated
    """
    if addon is None:
        print('Please provide an addon name')
    else:
        cfgfile = '%s/%s' % (site, filename)
        print 'Processing %s in %s' % (filename, site)
        config_parser = ConfigParser(dict_type=OrderedDict)
        config_parser.read(cfgfile)
        egglist = config_parser.get('eggs', 'addon')
        new_list = egglist + '\n%s' % addon
        config_parser.set('eggs', 'addon', new_list)
        for x in config_parser.sections():
            for name, value in config_parser.items(x):
                print '  %s = %r' % (name, value)
        with open(filename, 'wb') as configfile:
            config_parser.write(configfile)
        print 'Egglist for %s successfully updated' % site
