#!/usr/bin/python3
# Full deployment that creates and distributes an archive to web servers.

from fabric.api import *
import os.path
from datetime import datetime

# Set the fabric environment variables
env.hosts = ['100.26.238.151', '100.25.183.127']

def do_pack():
    """ generates a .tgz archive from the contents of  web_static"""

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    try:
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_name))
        return archive_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    Args: archive_path :: Path to archive to be distributed
    Return: If any error: Fale
            Otherwise: True
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """Creates and distributes an archives to  web servers."""
    archive_path = do_pack()
<<<<<<< HEAD
    if archive_path is None:
=======
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False

def deploy():
    """Full deployment of an archive to web servers"""
    file = do_pack()
    if file is None:
>>>>>>> e270a7800cc845db49a841f52bda84a30713aabb
        return False
    return do_deploy(archive_path)
