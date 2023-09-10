#!/usr/bin/python3
# Full deployment that creates and distributes an archive to web servers.

from fabric.api import *
import os.path
import os
from datetime import datetime

# Set the fabric environment variables
env.hosts = ['100.26.238.151', '100.25.183.127']

def do_pack():
    """
    Generate a .tgz archive from the contents of web_static
    folder into a .tgz archive.
    Returns:
        Archive path if successful, None upon failure
    """
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_" + timestamp + ".tgz"
        local("mkdir -p versions")
        local("tar -czvf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None


def do_deploy(archive_path):
    """Deploys the static files to the host servers

    Args:
        archive_path (str): The path of the archive to distribute
    """

    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """
    Full deployment of that static files to the servers
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
