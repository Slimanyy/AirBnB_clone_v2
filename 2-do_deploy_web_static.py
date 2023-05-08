#!/usr/bin/python3
""" a Fabric script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers, using the function do_deploy:

Prototype: def do_deploy(archive_path):
Returns False if the file at the path archive_path doesn’t exist
The script should take the following steps:
Upload the archive to the /tmp/ directory of the web server
Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
Delete the archive from the web server
Delete the symbolic link /data/web_static/current from the web server
Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
All remote commands must be executed on your both web servers (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
Returns True if all operations have been done correctly, otherwise returns False
You must use this script to deploy it on your servers: xx-web-01 and xx-web-02"""

from fabric.api import *
import os.path
from datetime import datetime

env.hosts = ['100.25.135.57', '54.242.163.85']
env.user = 'ubuntu'


def do_deploy(archive_path):
    if os.path.isfile(archive_path) is False:
        return False

    put(archive_path, '/tmp/')
    filename = archive_path.split('/')[-1]
    foldername = '/data/web_static/releases/' + filename.split('.')[0]
    run('mkdir -p {}'.format(foldername))
    run('tar -xzf /tmp/{} -C {} --strip-components=1'.format(filename, foldername))
    run('rm /tmp/{}'.format(filename))
    run('mv {}/web_static/* {}/'.format(foldername, foldername))
    run('rm -rf {}/web_static'.format(foldername))
    run('rm -f /data/web_static/current')
    run('ln -s {} /data/web_static/current'.format(foldername))

    return True
