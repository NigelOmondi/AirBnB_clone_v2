#!/usr/bin/python3
""" Fabric script to distribute an archive to web servers"""
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['100.26.238.151', '100.25.183.127']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


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

        return True
    except Exception:
        return False


if __name__ == "__main__":
    archive_path = do_pack()
    if archive_path:
        result = do_deploy(archive_path)
        if result:
            print("New version deployed!")
        else:
            print("Deployment failed.")
    else:
        print("Archive creation failed")
