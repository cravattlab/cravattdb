# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.ssh.forward_agent = true
  config.vm.network "forwarded_port", guest:8080, host:8080

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end

  config.vm.synced_folder "vagrant-sync/cimage-minimal", "/home/vagrant/github/cimage-minimal", create: true
  config.vm.synced_folder "vagrant-sync/cravattdb", "/home/vagrant/github/cravattdb", create: true

  config.vm.provision "dependencies", type: "shell", inline: <<-SHELL
    # installing things
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install -y git python-pip python3.5

    curl -sSL https://get.docker.com/ | sh
    sudo pip install docker-compose

    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash
    sudo apt-get install -y nodejs

    sudo npm install -g typescript@latest typings@latest

    # setup ssh
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    ssh-keyscan -H github.com >> ~/.ssh/known_hosts
    ssh -T git@github.com
  SHELL

  config.vm.provision "code", type: "shell", inline: <<-SHELL
    # don't forget the code
    git clone git@github.com:/cravattlab/cimage-minimal.git github/cimage-minimal
    git clone git@github.com:/cravattlab/cravattdb.git github/cravattdb
    chown -R vagrant:vagrant github
  SHELL

end