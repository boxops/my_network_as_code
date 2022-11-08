My Network as Code
==================

### (Work in Progress...)

A configuration management program that defines a network infrastructure in code using DevOps CI/CD practices.

Setup
-----

The Ansible control node was developed and tested on Ubuntu 22.04 LTS operating system.

```bash
$ git clone https://github.com/boxops/my_network_as_code.git
$ cd my_network_as_code
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install -r requirements.txt
```

Variables
---------

Before running playbooks, make sure to add your own unique variables in folders: ```group_vars```, ```host_vars```

and files: ```ansible.cfg```, ```staging_inventory.yml```, ```production_inventory.yml```.

Testing
-------

Lint playbooks, roles and collections:
```bash
$ ansible-lint deploy.yml
```

Validation
----------

Work in progress...

TODO: Verify and test functionality using Ansible roles for Batfish (https://github.com/batfish/ansible)

Production Deployment
---------------------

Run the ```deploy.yml``` playbook with the inventory file that defines production nodes:
```bash
$ ansible-playbook -i production_inventory.yml deploy.yml
```

License
-------

Apache License 2.0
