#!/usr/bin/python3
# Compress before sending

from fabric.api import *
from datetime import datetime


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
