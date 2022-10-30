# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

    config.vm.define "juniper" do |juniper|
        juniper.vm.box = "JunipervSRX3"
  
        #config.ssh.insert_key = false
        #config.vm.synched_folder ".", "/vagrant", disabled: true
    
        config.vm.provider :virtualbox do |v|
        v.memory = 4096
        v.linked_clone = true
    end

    config.vm.define "cisco" do |cisco|
        juniper.vm.box = "CiscoCSR1000v"
  
        #config.ssh.insert_key = false
        #config.vm.synched_folder ".", "/vagrant", disabled: true
    
        config.vm.provider :virtualbox do |v|
        v.memory = 4096
        v.linked_clone = true
    end

  # Provisioning configuration for Ansible.
    config.vm.provision "ansible_local" do |ansible|
      ansible.become = true
      ansible.playbook = "my_network_as_code/main.yml"
    end
  end
