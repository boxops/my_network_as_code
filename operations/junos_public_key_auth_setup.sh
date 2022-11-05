#!/bin/bash

# Bash Docstring (Not POSIX compliant)
DOC_REQUEST=70
if [ "$1" = "-h" -o "$1" = "--help"]; then
    cat <<DOCUMENTATION
Purpose:

    Silently generate an SSH key and append it to a remote Juniper node.

Requirements:

    The script assumes that the local DevBox has SSH access to the target
    Juniper node with username and password authentication.

Usage:

    Execute without sudo permissions:
    ./public_key_auth_setup.sh

DOCUMENTATION
exit $DOC_REQUEST
fi

# User prompts
DEFAULTREMOTEIP="10.1.1.1"
echo "Remote host IP or domain name:"
echo "Press enter for [$DEFAULTREMOTEIP]"
read REMOTEIP

DEFAULTSSHFILENAME="id_rsa"
echo "New SSH key filename:"
echo "Press enter for [$DEFAULTSSHFILENAME]"
read SSHFILENAME

DEFAULTREMOTEUSERNAME="admin"
echo "Remote host username:"
echo "Press enter for [$DEFAULTREMOTEUSERNAME]"
read REMOTEUSERNAME

DEFAULTREMOTEFILEPATH="/var/home/admin/"
echo "Remote host absolute filepath:"
echo "Press enter for [$DEFAULTREMOTEFILEPATH]"
read REMOTEFILEPATH

# Check if the key exists, create it if not
if [ ! -f ~/.ssh/$SSHFILENAME ] || [ ! -f ~/.ssh/$DEFAULTSSHFILENAME ]; then
    cd ~/.ssh
    ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/${SSHFILENAME:=$DEFAULTSSHFILENAME} <<<y >/dev/null 2>&1
    eval $(ssh-agent -s)
    ssh-add ~/.ssh/${SSHFILENAME:=$DEFAULTSSHFILENAME}
    echo "[ SSH key created. ]"
elif [ -f ~/.ssh/$SSHFILENAME ] || [ -f ~/.ssh/$DEFAULTSSHFILENAME ]; then
    echo "[ SSH key exists. ]"
else
    echo "[ Something went wrong. ]"
fi

echo "Uploading the key to the Juniper..."
scp ~/.ssh/${SSHFILENAME:=$DEFAULTSSHFILENAME}.pub ${REMOTEUSERNAME:=$DEFAULTREMOTEUSERNAME}@${REMOTEIP:=$DEFAULTREMOTEIP}:${REMOTEFILEPATH:=$DEFAULTREMOTEFILEPATH}

echo ""
echo "[ Follow the steps below to setup the Juniper for public key authentication. ]"
echo "1. Assign the ssh key to the user on the Juniper:"
echo "set system login user ${REMOTEUSERNAME:=$DEFAULTREMOTEUSERNAME} class super-user authentication load-key-file ${REMOTEFILEPATH:=$DEFAULTREMOTEFILEPATH}${SSHFILENAME:=$DEFAULTSSHFILENAME}.pub"
echo "2. Test your key from your DevBox:"
echo "ssh ${REMOTEUSERNAME:=$DEFAULTREMOTEUSERNAME}@${REMOTEIP:=$DEFAULTREMOTEIP}"
