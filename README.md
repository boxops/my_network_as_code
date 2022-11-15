My Network as Code
==================

### (Work in Progress...)

A configuration management program that defines a network infrastructure in code using DevOps CI/CD practices.

Setup
-----

The Ansible control node was developed and tested on Ubuntu 22.04 LTS operating system.

Clone the repository:
```bash
$ git clone https://github.com/boxops/my_network_as_code.git
```
Create a virtual environment:
```bash
$ cd my_network_as_code
$ python3 -m venv venv
$ source venv/bin/activate
```
Install required Python libraries:
```bash
$ python3 -m pip install -r requirements.txt
```

Variables
---------

Before running playbooks, make sure to add your own unique variables in folders: ```group_vars```, ```host_vars```

and files: ```staging_inventory.yml```, ```production_inventory.yml```.

Testing
-------

Lint playbooks, roles and collections:
```bash
$ ansible-lint deploy.yml
```

Validation
----------

Verify and test functionality using the Batfish interactive Python script:
```bash
$ python3 run_batfish_query.py
```

### Note:

The Batfish container needs to be installed and started on the Ansible control node before running the command above.

Follow the official guide to setup Batfish: https://batfish.readthedocs.io/en/latest/getting_started.html

Production Deployment
---------------------

Run the ```deploy_network.yml``` playbook with the inventory file that defines production nodes:
```bash
$ ansible-playbook -i production_inventory.yml deploy_network.yml
```

New Feature
-----------

Assemble your configuration files using Ansible before deploying them.

This feature builds commands using templates and saves the output to files within the ```builds``` directory where Batfish can load them and create a vendor-neutral model ready for developers to query services that will be running on nodes.

Run the ```assemble_builds.yml``` playbook to assemble your own configuration files:
```bash
$ ansible-playbook -i production_inventory.yml assemble_builds.yml
```

License
-------

Apache License 2.0
