#!/usr/bin/python3
"""script that creates and distributes the function deploy to the web servers
"""
from fabric.api import *
import os.path
from datetime import datetime

env.hosts = ['34.203.75.215', '54.175.88.234']
env.user = 'ubuntu'


def do_pack():
    """generates a .tgz from html folder"""
    # creates the versions directory
    local('mkdir -p versions')

    dnow = datetime.now()
    archive_name = 'web_static_{}{}{}{}{}{}.tgz'.format(dnow.year, dnow.month,
                                                        dnow.day, dnow.hour,
                                                        dnow.minute,
                                                        dnow.second)
    # create archive and store it in the version directory
    arch_store = local("tar -cvzf versions/{} web_static".format(archive_name))

    if arch_store.succeeded:
        return 'versions/{}'.format(archive_name)
    else:
        return None


def do_deploy(archive_path):
    """deploys and distributes archive"""
    if os.path.isfile(archive_path) is False:
        return False

    # Extract the archive to the new folder on the server
    filename = archive_path.split('/')[-1]
    name = filename.split('.')[0]

    put(archive_path, "/tmp/{}".format(filename))
    run('mkdir -p /data/web_static/releases/{}/'.format(name))
    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
        .format(filename, name))

    # Remove the archive from the server
    run('rm /tmp/{}'.format(filename))

    # Move the contents of the web_static folder to the new folder
    run("mv /data/web_static/releases/{}/web_static/* "
        "/data/web_static/releases/{}/"
        .format(name, name))
    run('rm -rf /data/web_static/releases/{}/web_static'.format(name))

    # Delete the symbolic link to the current version and create a new one
    run('rm -f /data/web_static/current')
    run('ln -s /data/web_static/releases/{} /data/web_static/current'
        .format(name))
    print("New version deployed!")

    return True


def deploy():
    """call do_pack and do_deploy functions"""
    archiv_path = do_pack()
    if archiv_path is None:
        return False
    return do_deploy(archiv_path)
