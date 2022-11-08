#!/usr/bin/env python3
import os
import subprocess
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP
from jnpr.junos.utils.config import Config

# User prompts
default_remote_ip = "10.1.1.1"
remote_ip = input(f"Remote host IP or domain name [{default_remote_ip}]: ") or default_remote_ip

default_ssh_filename = "id_rsa"
ssh_file_name = input(f"New SSH key filename [{default_ssh_filename}]: ") or default_ssh_filename

default_remote_username = "admin"
remote_username = input(f"Remote host username [{default_remote_username}]: ") or default_remote_username

remote_password = getpass("Remote host password: ")

default_remote_file_path = "/var/home/admin/"
remote_file_path = input(f"Remote host absolute filepath [{default_remote_file_path}]: ") or default_remote_file_path


# Check if the key exists, create it if not
key_path = os.path.expanduser(f"~/.ssh/{ssh_file_name}")
file_exists = os.path.exists(key_path)

if file_exists is False:
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-N", '', "-f", f"{key_path}"], stdout=subprocess.DEVNULL)
    subprocess.run(["ssh-add", f"{key_path}"])
else:
    print("Key exists.")

# Copy over the local public key to the Junos
# subprocess.run(["scp", f"{key_path}.pub", f"{remote_username}@{remote_ip}:{remote_file_path}"])

device_port = "830"
device = Device(host=default_remote_ip, user=remote_username, password=remote_password, port=device_port)
with SCP(device) as scp:
    scp.put(f"{key_path}.pub", remote_path=remote_file_path)

# Assign the SSH key to the user on the Junos (configuration)
set_command = f"set system login user {remote_username} class super-user authentication load-key-file {remote_file_path}{ssh_file_name}.pub"
with Config(device, mode="private") as cu:
    cu.open()
    cu.load(set_command)
    cu.commit()
device.close()
