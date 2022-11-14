#!/usr/bin/env python3

import os
import subprocess
from getpass import getpass
from netmiko import ConnectHandler, file_transfer

'''
Purpose:

    Silently generate an SSH key and append it to a remote Juniper node.

Requirements:

    The script assumes that the local Ansible control node has SSH access
    to the target Juniper node with username and password authentication.

Usage:

    Run the script without sudo permissions:
    python3 public_key_auth_setup.py
'''

# User prompts
default_remote_ip = "10.1.1.1"
remote_ip = input(f"Remote host IP or domain name [{default_remote_ip}]: ") or default_remote_ip

default_ssh_filename = "id_rsa"
ssh_file_name = input(f"New SSH key filename [{default_ssh_filename}]: ") or default_ssh_filename
public_ssh_file_name = f"{ssh_file_name}.pub"

default_remote_username = "ansible"
remote_username = input(f"Remote host username [{default_remote_username}]: ") or default_remote_username

remote_password = getpass("Remote host password: ")

default_remote_file_path = "/var/home/ansible/"
remote_file_path = input(f"Remote host absolute filepath [{default_remote_file_path}]: ") or default_remote_file_path

# Check if the SSH key exists, create it if not
key_path = os.path.expanduser(f"~/.ssh/{ssh_file_name}")
file_exists = os.path.exists(key_path)

if file_exists is False:
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-N", '', "-f", f"{key_path}"], stdout=subprocess.DEVNULL)
    subprocess.check_output(["ssh-agent", "-s"])
    subprocess.run(["ssh-add", f"{key_path}"])
else:
    print("Key exists.")

device = {
    "device_type": "juniper_junos",
    "host": remote_ip,
    "username": remote_username,
    "password": remote_password,
    "port": 22
}

# Copy over the local public SSH key to the Juniper
connect = ConnectHandler(**device)

transfer = file_transfer(
    connect,
    source_file=f"{key_path}.pub",
    dest_file=public_ssh_file_name,
    file_system=remote_file_path,
    direction="put",
    overwrite_file=True
)

# Assign the SSH key to the user on the Juniper (configuration)
command = f"set system login user {remote_username} class super-user authentication load-key-file {remote_file_path}{ssh_file_name}.pub"
config = connect.send_config_set(command)
config = connect.commit()
print(config)
