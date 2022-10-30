My Network as Code
==================

A configuration management program that defines a network infrastructure in code using DevOps CI/CD practices.

Setup
-----

Tested on Ubuntu 22.04 operating system.
```bash
$ git clone https://github.com/boxops/my_network_as_code.git
$ cd my_network_as_code
```

Requirements
------------

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install requirements.txt
```

Variables
---------

Make sure to use your own unique variables in ```vars/all.yml``` file and also update the path to the SSH private key file in ```ansible.cfg```.

Testing
-------

Lint playbooks, roles and collections:
```bash
$ ansible-lint playbook.yml
```

Validation
----------

Deploy and validate Ansible tasks using Vagrant that starts a VM and runs the provisioning playbook:
```bash
$ vagrant up
```

Production Deployment
---------------------

Run the main playbook with the inventory file that defines production nodes:
```bash
$ ansible-playbook -i production_inventory.ini main.yml
```

License
-------

Apache License 2.0
