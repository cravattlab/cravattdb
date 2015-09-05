# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.ssh.forward_agent = true

  config.vm.synced_folder "vagrant-sync/cimage-minimal", "/home/vagrant/github/cimage-minimal", create: true
  config.vm.synced_folder "vagrant-sync/cravatt-ip2", "/home/vagrant/github/cravatt-ip2", create: true

  config.vm.provision "shell", inline: <<-SHELL
    # installing things
    sudo apt-get update
    sudo apt-get install -y git python-pip
    curl -sSL https://get.docker.com/ | sh
    sudo pip install docker-compose

    # setup ssh
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    ssh-keyscan -H github.com >> ~/.ssh/known_hosts
    ssh -T git@github.com

    # don't forget the code
    git clone git@github.com:/cravattlab/cimage-minimal.git github/cimage-minimal
    git clone git@github.com:/cravattlab/cravatt-ip2.git github/cravatt-ip2
    chown -R vagrant:vagrant github
  SHELL

end