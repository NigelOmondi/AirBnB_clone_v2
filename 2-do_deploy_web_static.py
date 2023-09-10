#!/usr/bin/python3
""" Fabric script to distribute an archive to remote web servers"""

from fabric.api import *
import os
from os import path
from datetime import datetime

env.hosts = ['100.26.238.151', '100.25.183.127']

def do_deploy(archive_path):
    """"Deploy an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        """Upload archive to /tmp/"""
        put(archive_path, "/tmp/")

        """Get archive filename without extension"""
        archive_filename = archive_path.split("/")[-1].split(".")[0]

        """Create folder /data/web_static/releases/<archive_filename>"""
        run("mkdir -p /data/web_static/releases/{}".format(archive_filename))

        """Uncompress the archive"""
        run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}".format(
           archive_filename, archive_filename))

        """Remove the archive from /tmp/"""
        run("rm /tmp/{}.tgz".format(archive_filename))

        """Move the contents of the folder to its parent directory"""
        run("mv /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}".format(archive_filename, archive_filename))

        """Remove the old symbolic link"""
        run("rm -rf /data/web_static/current")

        """Create a new symbolic link"""
        run("ln -s /data/web_static/releases/{} \
             /data/web_static/current".format(archive_filename))

        puts("New version deployed!")
        return True
    except Exception:
        return False
