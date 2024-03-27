#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

# Define the hosts (web servers) to deploy to
env.hosts = ["54.237.32.44", "35.175.128.148"]

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    # Step 1: Check if the archive file exists
    if os.path.isfile(archive_path) is False:
        return False
    
    # Extract the filename and name of the archive without extension
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Step 2: Upload the archive to the /tmp/ directory on the remote server
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    
    # Step 3: Remove existing release directory, create new directory, and extract the archive
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed is True:
        return False
    
    # Step 4: Remove the uploaded archive from /tmp/
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    
    # Step 5: Move contents of web_static/ to the release directory, cleanup web_static directory
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed is True:
        return False
    
    # Step 6: Remove existing symbolic link and create a new one pointing to the new release directory
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed is True:
        return False
    
    # Step 7: Return True if all steps completed successfully
    return True

