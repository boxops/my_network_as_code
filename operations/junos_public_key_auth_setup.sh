#!/bin/bash

# Purpose: Silently generate an SSH key and append it to a remote Juniper node.

# Requirements: The script assumes that the local DevBox has SSH access to the target Juniper node.

# Usage: Execute without sudo permissions.
# ./public_key_auth_setup.sh

DEFAULTSSHFILENAME="id_rsa"
echo "New SSH key filename:"
echo "Press enter for [$DEFAULTSSHFILENAME]"
read SSHFILENAME

DEFAULTREMOTEIP="10.1.1.1"
echo "Remote host IP:"
echo "Press enter for [$DEFAULTREMOTEIP]"
read REMOTEIP

DEFAULTREMOTEUSERNAME="admin"
echo "Remote host username:"
echo "Press enter for [$DEFAULTREMOTEUSERNAME]"
read REMOTEUSERNAME

DEFAULTREMOTEFILEPATH="/var/home/admin/"
echo "Remote host absolute filepath:"
echo "Press enter for [$DEFAULTREMOTEFILEPATH]"
read REMOTEFILEPATH

cd ~/.ssh

ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/${SSHFILENAME:=$DEFAULTSSHFILENAME} <<<y >/dev/null 2>&1

eval $(ssh-agent -s)

ssh-add ~/.ssh/${SSHFILENAME:=$DEFAULTSSHFILENAME}

scp ~/.ssh/${SSHFILENAME:=$DEFAULTSSHFILENAME}.pub ${REMOTEUSERNAME:=$DEFAULTREMOTEUSERNAME}@${REMOTEIP:=$DEFAULTREMOTEIP}:${REMOTEFILEPATH:=$DEFAULTREMOTEFILEPATH}

echo ""
echo "[ SSH Key created. Follow the steps below to setup the Juniper for public key authentication. ]"
echo "1. Assign the ssh key to the user on the Juniper:"
echo "set system login user ${REMOTEUSERNAME:=$DEFAULTREMOTEUSERNAME} class super-user authentication load-key-file ${REMOTEFILEPATH:=$DEFAULTREMOTEFILEPATH}${SSHFILENAME:=$DEFAULTSSHFILENAME}.pub"
echo "2. Test your key from your DevBox:"
echo "ssh ${REMOTEUSERNAME:=$DEFAULTREMOTEUSERNAME}@${REMOTEIP:=$DEFAULTREMOTEIP}"
