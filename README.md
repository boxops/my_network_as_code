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

Production Deployment
---------------------

Run the ```deploy_network.yml``` playbook with the inventory file that defines production nodes:
```bash
$ ansible-playbook -i production_inventory.yml deploy_network.yml
```

License
-------

Apache License 2.0
